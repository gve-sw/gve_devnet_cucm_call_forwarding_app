# GVE DevNet CUCM Call Forwarding App
This repository contains the source code of a Flask app that can set the call forwarding number for phones associated with CUCM. As written, the code will set the call forwarding busy external and internal, call forwarding no answer external and internal, and the call forwarding unregistered external and internal within CUCM to the number entered in the web form.

![/IMAGES/workflow.png](/IMAGES/workflow.png)

## Contacts
* Danielle Stacy

## Solution Components
* Python 3.11
* CUCM
* Flask
* [Zeep](https://github.com/CiscoDevNet/axl-python-zeep-samples)

## Prerequisites
**CUCM Credentials:** In order to use the CUCM APIs, you need to make note of the IP address, username, and password of your instance of CUCM. Note these values to add to the environmental variables file (.env) during the installation phase.

**Floor to Extension Number Mapping:** If you would like to display floor names that have pre-set extension numbers rather than requiring the user to enter an extension number themselves, set the INCLUDE_MAP variable in app.py on line 38 to True. Additionally, provide the mappings from floor to extension in the file extension-mapping.json:
```
{
    "floor name 1": "extension number",
    "floor name 2": "extension number",
    "floor name 3": "extension number"
}
```

**Call Forwarding Options:** If you would like to change which CUCM call forwarding settings are changed, then modify the code in app.py on lines 109-114. For instance, if you would like to set the call forwarding all number, then add the line:
```python
callForwardAll=forward_info
```

## Installation/Configuration
1. Clone this repository with the command `git clone [repository name]`. To find the repository name, click the green `Code` button at the top right corner of the page. Then copy the HTTPS URL, as seen here.
![/IMAGES/clone-command.png](/IMAGES/clone-command.png)
2. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).
3. Install the requirements with the command `pip3 install -r requirements.txt`.
4. Add the IP address, username, and password of your CUCM environment to the .env file.
```python
CUCM_ADDRESS="enter IP address here"
AXL_USERNAME="enter username here"
AXL_PASSWORD="enter password here"
```

## Usage
To start the web app, run the command:
```
$ flask run
```
Then access the web app in the browser of your choice at the address `http://127.0.0.1:5000`. From here, you will be presented with a form where you can enter the number that you wish to set call forwarding for and the number to which you wish to forward calls.
![/IMAGES/no-floors-form.png](/IMAGES/no-floors-form.png)
If you have specified a JSON file mapping floors to extension numbers, then you will be presented with a dropdown select menu of the floors.
![/IMAGES/floors-form.png](/IMAGES/floors-form.png)

Once you have filled out the form and hit submit, the backend will set the forwarding number in CUCM. If the forwarding number is successfully set, then the page will reload the form with a success message. Otherwise, an error message will display.

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.