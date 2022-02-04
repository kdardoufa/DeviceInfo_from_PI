#from primeapidata import PI_ADDRESS, USERNAME, PASSWORD
from PrimeDeviceFunctions import getDevices, getDeviceGroups, RemoveGeneric, writeDevices
import logging

def main():
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    filename='GetAllDevices.log', level=logging.INFO)
    logging.info("Begin")
    InitialGroups = getDeviceGroups()
    Groups = RemoveGeneric(InitialGroups)
    DevicesList = getDevices(Groups)
    writeDevices(DevicesList)
    logging.info("End")
    return()


if __name__ == "__main__":
    main()
