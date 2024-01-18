import csv
from datetime import datetime, timedelta

# Load CSV files
with open('C:/Users/jamal/Downloads/addressCSV.csv') as addyCSV:
    AddressCSV = csv.reader(addyCSV)
    AddressCSV = list(AddressCSV)
with open('C:/Users/jamal/Downloads/distanceCSV.csv') as disCSV:
    DistanceCSV = csv.reader(disCSV)
    DistanceCSV = list(DistanceCSV)


# Hash Table class
class CreateHashTable:
    def __init__(self, initialcapacity=40):
        self.table = []
        for i in range(initialcapacity):
            self.table.append([])

    # Inserts a new item into the hash table and will update an item in the list already
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # update key if  already in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        # if not found in the bucket, insert item to the end
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches the hash table for an item with the matching key
    # Will return the item if found, or none if not found
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # search for key in bucket
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]  # value
        return None

        # Removes  item with matching key

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # removes the item if it is present
        if key in bucket_list:
            bucket_list.remove(key)


# Package class
class Packages:
    def __init__(self, ID, street, city, state, zip, deadline, weight, notes, status, departureTime, deliveryTime):
        self.ID = ID
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.departureTime = None
        self.deliveryTime = None

    def __str__(self):
        return "ID: %s, %-20s, %s, %s,%s, Deadline: %s,%s,%s,Departure Time: %s,Delivery Time: %s" % (
            self.ID, self.street, self.city, self.state, self.zip, self.deadline, self.weight, self.status,
            self.departureTime, self.deliveryTime)

    def statusUpdate(self, timeChange):
        if self.deliveryTime == None:
            self.status = "At the hub"
        elif timeChange < self.departureTime:
            self.status = "At the hub"
        elif timeChange < self.deliveryTime:
            self.status = "En route"
        else:
            self.status = "Delivered"
        if self.ID == 9:  # package 9 address will change correctly once delivered
            if timeChange > timedelta(hours=10, minutes=20):
                self.street = "410 S State St"
                self.zip = "84111"
            else:
                self.street = "300 State St"
                self.zip = "84103"

def loadPackageData(filename):
    with open(filename) as packagess:
        packageInfo = csv.reader(packagess, delimiter=',')
        next(packageInfo)
        for package in packageInfo:
            pID = int(package[0])
            pStreet = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pNotes = package[7]
            pStatus = "At the Hub"
            pDepartureTime = None
            pDeliveryTime = None

            # Package info
            p = Packages(pID, pStreet, pCity, pState, pZip, pDeadline, pWeight, pNotes, pStatus, pDepartureTime,
                         pDeliveryTime)

            packageHash.insert(pID, p)


# Hash table for packages
packageHash = CreateHashTable()


# Truck class
class Trucks:
    def __init__(self, speed, miles, currentLocation, departTime, packages):
        self.speed = speed
        self.miles = miles
        self.currentLocation = currentLocation
        self.time = departTime
        self.departTime = departTime
        self.packages = packages

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s" % (
            self.speed, self.miles, self.currentLocation, self.time, self.departTime, self.packages)


# minimum distance for the next address
def addresss(address):
    for row in AddressCSV:
        if address in row[2]:
            return int(row[0])


# distance between two addresses
def Betweenst(addy1, addy2):
    distance = DistanceCSV[addy1][addy2]
    if distance == '':
        distance = DistanceCSV[addy2][addy1]
    return float(distance)


# pulls data from CSV into the function
loadPackageData('C:/Users/jamal/Downloads/packageCSV.csv')

# manually loading the trucks and assigning them a departure time
truck1 = Trucks(18, 0.0, "4001 South 700 East", timedelta(hours=8),
                [1, 13, 14, 15, 16, 19, 20, 27, 29, 30, 31, 34, 37, 40])
truck2 = Trucks(18, 0.0, "4001 South 700 East", timedelta(hours=11),
                [2, 3, 4, 5, 9, 18, 26, 28, 32, 35, 36, 38])
truck3 = Trucks(18, 0.0, "4001 South 700 East", timedelta(hours=9, minutes=5),
                [6, 7, 8, 10, 11, 12, 17, 21, 22, 23, 24, 25, 33, 39])


# package delivery algorithm
def truckDeliverPackages(truck):
    # create a list for  the packages that have to be delivered
    enroute = []
    # put packages in en route list from hash table
    for packageID in truck.packages:
        package = packageHash.search(packageID)
        enroute.append(package)

    truck.packages.clear()
    # while packages is true, the algo will run still
    while len(enroute) > 0:
        nextAddy = 2000
        nextPackage = None
        for package in enroute:
            if package.ID in [25, 6]:
                nextPackage = package
                nextAddy = Betweenst(addresss(truck.currentLocation), addresss(package.street))
                break
            if Betweenst(addresss(truck.currentLocation), addresss(package.street)) <= nextAddy:
                nextAddy = Betweenst(addresss(truck.currentLocation), addresss(package.street))
                nextPackage = package
        truck.packages.append(nextPackage.ID)
        enroute.remove(nextPackage)
        truck.miles += nextAddy
        truck.currentLocation = nextPackage.street
        truck.time += timedelta(hours=nextAddy / 18)
        nextPackage.deliveryTime = truck.time
        nextPackage.departureTime = truck.departTime


def parse_time(time_str):
    """Parse a time string in HH:MM format and return a datetime.timedelta object."""
    try:
        h, m = map(int, time_str.split(":"))
        return timedelta(hours=h, minutes=m)
    except ValueError:
        print("Invalid time format. Please enter in HH:MM format.")
        return None

def display_status_in_time_range(start_time_str, end_time_str):
    start_time = parse_time(start_time_str)
    end_time = parse_time(end_time_str)
    if start_time is None or end_time is None:
        return  # Exit the function if time parsing failed

    print(f"\nStatus of packages between {start_time_str} and {end_time_str}:")
    for packageID in range(1, 41):
        package = packageHash.search(packageID)
        if package:  # Check if the package exists
            package.statusUpdate(end_time)  # Update status at the end time
            # Check if package departure or delivery time is within the time range
            if start_time <= package.departureTime <= end_time or start_time <= package.deliveryTime <= end_time:
                print(str(package))
    total_miles = truck1.miles + truck2.miles + truck3.miles
    print("\nTotal miles traveled by all trucks:", total_miles)

# Deliver the packages
truckDeliverPackages(truck1)
truckDeliverPackages(truck3)
truck2.departTime = min(truck1.time, truck3.time)
truckDeliverPackages(truck2)

# Command-line interface
while True:
    start_time = input("\nEnter the start time to check package status (format HH:MM), or type 'exit' to quit: ")
    if start_time.lower() == 'exit':
        break
    end_time = input("Enter the end time to check package status (format HH:MM): ")
    if end_time.lower() == 'exit':
        break
    display_status_in_time_range(start_time, end_time)


