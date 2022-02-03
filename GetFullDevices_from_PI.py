from primeapidata import PI_ADDRESS, USERNAME, PASSWORD
from PrimeDeviceFunctions import getDevices, getDeviceGroups, RemoveGeneric

def main():
    InitialGroups = getDeviceGroups()
    Groups = RemoveGeneric(InitialGroups)
    getDevices(Groups)
    return()


if __name__ == "__main__":
    main()
