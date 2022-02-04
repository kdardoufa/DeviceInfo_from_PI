from primeapidata import PI_ADDRESS, USERNAME, PASSWORD
from PrimeDeviceFunctions import getDevices, getDeviceGroups, RemoveGeneric, writeDevices

def main():
    InitialGroups = getDeviceGroups()
    Groups = RemoveGeneric(InitialGroups)
    DevicesList = getDevices(Groups)
    writeDevices(DevicesList)

    return()


if __name__ == "__main__":
    main()
