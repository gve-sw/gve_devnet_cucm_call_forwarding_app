""" Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

# Import Section
from flask import Flask, render_template, request, url_for, redirect
from lxml import etree
from zeep import Client, Settings, Plugin, xsd
from zeep.transports import Transport
from zeep.exceptions import Fault
from collections import defaultdict
from requests import Session
from requests.auth import HTTPBasicAuth
import requests
import datetime
import json
import os
import sys
import urllib3
from dotenv import load_dotenv

# load all environment variables
load_dotenv()


# Global variables

# If True, provide floor names and extension numbers in extension-mapping.json
INCLUDE_MAP = True

# Change to true to enable output of request/response headers and XML
DEBUG = True

# The WSDL is a local file in the working directory, see README
WSDL_FILE = 'schema/AXLAPI.wsdl'

# The first step is to create a SOAP client session
session = Session()

# We avoid certificate verification by default
# And disable insecure request warnings to keep the output clear
session.verify = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# To enabled SSL cert checking (recommended for production)
# place the CUCM Tomcat cert .pem file in the root of the project
# and uncomment the line below

# session.verify = 'changeme.pem'

# Add Basic Auth credentials
session.auth = HTTPBasicAuth(os.getenv('AXL_USERNAME'),
                             os.getenv('AXL_PASSWORD'))

# Create a Zeep transport and set a reasonable timeout value
transport = Transport(session=session, timeout=10)

# strict=False is not always necessary, but it allows zeep to parse imperfect XML
settings = Settings(strict=False, xml_huge_tree=True)

# This class lets you view the incoming and outgoing http headers and XML

class MyLoggingPlugin( Plugin ):

    def egress( self, envelope, http_headers, operation, binding_options ):

        # Format the request body as pretty printed XML
        xml = etree.tostring( envelope, pretty_print = True, encoding = 'unicode')

        print( f'\nRequest\n-------\nHeaders:\n{http_headers}\n\nBody:\n{xml}' )

    def ingress( self, envelope, http_headers, operation ):

        # Format the response body as pretty printed XML
        xml = etree.tostring( envelope, pretty_print = True, encoding = 'unicode')

        print( f'\nResponse\n-------\nHeaders:\n{http_headers}\n\nBody:\n{xml}' )


# If debug output is requested, add the MyLoggingPlugin callback
plugin = [MyLoggingPlugin()] if DEBUG else []

# Create the Zeep client with the specified settings
client = Client(WSDL_FILE, settings=settings, transport=transport,
        plugins=plugin)

# Create the Zeep service binding to AXL at the specified CUCM
service = client.create_service('{http://www.cisco.com/AXLAPIService/}AXLAPIBinding',
                                f'https://{os.getenv( "CUCM_ADDRESS" )}:8443/axl/')


app = Flask(__name__)

# Methods
# update the forwarding number in CUCM
def update_line(pattern, destination):
    forward_info = {
        "destination": destination
    }
    try:
        resp = service.updateLine(pattern=pattern, callForwardBusy=forward_info,
                                  callForwardBusyInt=forward_info,
                                  callForwardNoAnswer=forward_info,
                                  callForwardNoAnswerInt=forward_info,
                                  callForwardNotRegistered=forward_info,
                                  callForwardNotRegisteredInt=forward_info)
    except Fault as err:
        print(f"Zeep error: updateLine: { err }")
        return False

    print("\nupdateLine response:\n")
    print(resp, "\n")

    return True


##Routes
#Instructions

#Index
@app.route('/', methods=['GET', 'POST'])
# main page
def index():
    try:
        # if there is a json file that maps the floors to extension numbers
        if INCLUDE_MAP:
            with open("extension-mapping.json") as f:
                extensions = json.load(f)
                floors = extensions.keys()
        # otherwise, floors will just be an empty list that isn't used
        else:
            floors = []

        # the form has been submitted to change the forwarding number
        if request.method == 'POST':
            # get the phone number that needs its forwarding number changed
            phone_num = request.form.get('phone-num')

            # if there is a json file mapping floors to extension numbers, then we need to get what selection the user made from a dropdown menu of the floors and then select the extension number associated with that floor
            if INCLUDE_MAP:
                forwarding_floor = request.form.get('forwarding-num-select')
                forwarding_num = extensions[forwarding_floor]
            # otherwise, the user will just enter the number they wish to forward their calls to
            else:
                forwarding_num = request.form.get('forwarding-num')

            # update the forwarding number with the form values
            update_status = update_line(phone_num, forwarding_num)

            # if all was successful, the form page will display a success message
            if update_status:
                return render_template('form.html', hiddenLinks=False,
                                       success=True,
                                       phone_num=phone_num,
                                       forwarding_num=forwarding_num,
                                       include_map=INCLUDE_MAP,
                                       floors=floors)
            else:
                return render_template('form.html', hiddenLinks=False,
                                       error=True,
                                       errormessage="There was an issue updating " + phone_num + " with the forwarding num " + forwarding_num,
                                       errorcode="API call failed")

        return render_template('form.html', hiddenLinks=False,
                               include_map=INCLUDE_MAP,
                               floors=floors)
    except Exception as e:
        print(e)
        #OR the following to show error message
        return render_template('form.html', error=True, errormessage="There was an issue with the app", errorcode=e)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
