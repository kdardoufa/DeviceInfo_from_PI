import requests
import json
import csv
import logging
from requests.auth import HTTPBasicAuth
import time

# Define Global Variables
USERNAME = "username"  # define  REST API username
PASSWORD = "password"  # define REST API passowrd
PI_ADDRESS = "ip_address"  # define IP Address of Prime Infrastructure Server

requests.packages.urllib3.disable_warnings()

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='GetAllDevices.log', level=logging.INFO)

controller_url = "https://"+PI_ADDRESS+"/webacs/api/v4/data/InventoryDetails/"
Group_List = []

timestr = time.strftime("%Y%m%d_%H%M")
Device_List = "DeviceList_"+timestr+".csv"


def getDeviceGroups():
    logging.info(" - Getting all device groups")
    url = "https://"+PI_ADDRESS+"/webacs/api/v2/data/DeviceGroups.json"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), verify=False)
    r_json = response.json()
    Group_List = []
    group = "dummy value"
    for entity in r_json['queryResponse']['entityId']:
        for value in entity.values():
            if "https" in value:
                new_url = value + ".json"
                # print(new_url)
                group_response = requests.get(
                    new_url, auth=HTTPBasicAuth(USERNAME, PASSWORD), verify=False)
                group_json = group_response.json()
                # print(new_url)
                dev_dict = group_json["queryResponse"]["entity"][0]
                deviceGroupsDTO = dev_dict.get("deviceGroupsDTO", "None")
                group = deviceGroupsDTO.get("groupName", "")
                time.sleep(1)
                Group_List.append(group)
                logging.info(f' - {group} added to list')
    logging.info(" - Initial groups ok... moving on")
    return(Group_List)
# End of Function


def RemoveGeneric(Group_List):
    #if thing in some_list: some_list.remove(thing)
    logging.info(" - Removing Generic Groups")
    if "Device Type" in Group_List:
        Group_List.remove("Device Type")
    if "Routers" in Group_List:
        Group_List.remove("Routers")
    if "Security and VPN" in Group_List:
        Group_List.remove("Security and VPN")
    if "Switches and Hubs" in Group_List:
        Group_List.remove("Switches and Hubs")
    if "Unified AP" in Group_List:
        Group_List.remove("Unified AP")
    if "Unsupported Cisco Device" in Group_List:
        Group_List.remove("Unsupported Cisco Device")
    if "Wireless Conteroller" in Group_List:
        Group_List.remove("Wireless Contoroller")
    new_Group_List = Group_List
    logging.info(" - Final groups ok... moving on")
    return(new_Group_List)
# End of Function


def getDevices(Group_List):
    logging.info(" - Getting Device Info")
    i = 0
    NumOfGroups = len(Group_List)
    # open a file for writing
    DeviceList = open(Device_List, 'w')
    # create the csv writer object
    csvwriter = csv.writer(DeviceList)
    header = ["DeviceName", "IP_Address", "Location", "Type", "Serial Number"]
    csvwriter.writerow(header)
    while i < NumOfGroups:
        group = Group_List[i]
        url = controller_url + ".json?.group=" + group
        response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), verify=False)
        r_json = response.json()
        try:
            count = (r_json.get("queryResponse", "")).get("@count", "")
            if count == 0:
                # Move on to next group
                i += 1
                continue
            else:
                logging.info(f' - Getting devices in group {group}')
                for entity in r_json['queryResponse']['entityId']:
                    for value in entity.values():
                        if "https" in value:
                            new_url = value + ".json"
                            # print(new_url)
                            device_response = requests.get(
                                new_url, auth=HTTPBasicAuth(USERNAME, PASSWORD), verify=False)
                            device_json = device_response.json()
                            response = device_json.get("queryResponse", "")
                            if (type(response) != str)and(group != "Unsupported Cisco Device"):
                                for key in response:
                                    if key == "entity":
                                        value = response[key][0]
                                        Info = value.get("inventoryDetailsDTO", "")
                                        SN = (((Info.get("chassis", "")).get("chassis", ""))
                                              [0]).get("serialNr", "")
                                        Model = (((Info.get("chassis", "")).get(
                                            "chassis", ""))[0]).get("modelNr", "")
                                        DeviceName = (Info.get("summary", "")).get("deviceName", "")
                                        IP_Addr = (Info.get("summary", "")).get("ipAddress", "")
                                        Location = (Info.get("summary", "")).get("location", "")
                                        DevType = (Info.get("summary", "")).get("devicType", "")
                                        new_row = [DeviceName, IP_Addr, Location, Model, SN]
                                csvwriter.writerow(new_row)
                            elif (type(response) != str)and(group == "Unsupported Cisco Device"):
                                for key in response:
                                    if key == "entity":
                                        value = response[key][0]
                                        Info = value.get("inventoryDetailsDTO", "")
                                        DeviceName = (Info.get("summary", "")).get("deviceName", "")
                                        IP_Addr = (Info.get("summary", "")).get("ipAddress", "")
                                        Location = (Info.get("summary", "")).get("location", "")
                                        DevType = (Info.get("summary", "")).get("devicType", "")
                                        SN = (Info.get("summary", "")).get("serialNr", "-")
                                        Model = (Info.get("summary", "")).get("modelNr", "-")
                                new_row = [DeviceName, IP_Addr, Location, Model, SN]
                                csvwriter.writerow(new_row)
                            else:
                                continue
        except:
            logging.info(" - Moving on to next group - due to error")
            continue
        # exit try
        # Moving on to next Group - still inside while loop
        i += 1

    logging.info(" - All info has been collected.\nEND")
    DeviceList.close()
    return()
# End of function


def main():
    InitialGroups = getDeviceGroups()
    Groups = RemoveGeneric(InitialGroups)
    getDevices(Groups)
    return()


if __name__ == "__main__":
    main()
