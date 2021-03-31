
## Description 

Use Cisco Prime Infrastructure 3.5 REST APIs to get information about the Hostname/Mgmt IP Address/ SNMP Location/SerialNumber of all devices monitored by the PI. The script does the following:
-	Gets all the device type groups (Routers/4300/4200/Switches etc). Function getDeviceGroups is used for this purpose.
-	Any group that is considered as a parent directory is removed. Function RemoveGeneric is used for this purpose.
-	Function getDevices iterates through the groups and gathers the required information. If the group is empty, it moves on to the next group.
The information is written into a csv file, in order to be used as input into another application. The csv created has a naming convention of:
DeviceList_current_date_time.csv. 
The primary goal was to gather the information and feed it into netbox.

# Configuration
The user should define the following in a file named primeapidata.py, according to their environment.
- USERNAME: define REST API username
- PASSWORD: define REST API password
- PI_ADDRESS: define IP Address of Prime Infrastructure Server

It's also possible to comment out the import of those variables and instead define them as global variables. If that is your choice, comment out  the commands:
```python
#USERNAME = "username"  # define  REST API username
#PASSWORD = "password"  # define REST API passowrd
#PI_ADDRESS = "ip_address"  # define IP Address of Prime Infrastructure Server
```

# Technologies & Frameworks Used
* Prime Infratructure APIs are used.
* NO Third-Party products or Services are used.
* The script is written in Python 3.

# Installation
1. Clone the repo
  * git clone https://github.com/kdardoufa/DeviceInfo_from_PI.git

2. cd into directory
  * cd DeviceInfo_from_PI

3. Create the virtual environment in a sub dir in the same directory
  * python3 -m venv venv

4. Start the virtual environment and install requirements.txt
  * source venv/bin/activate
  * pip install -r requirements.txt

5. Execute the script as any other Python script form console. 
  * python getFullDevices_from_PI.py

# Known issues
No Issues found

# Author(s)
This project was written and is maintained by the following individuals
> Katerina Dardoufa (kdardoufa@gmail.com)


[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/kdardoufa/DeviceInfo_from_PI)
