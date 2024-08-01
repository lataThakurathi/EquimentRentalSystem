# defining function to get file content
def readEquipmentFile():
    file = open("equipments.txt", "r")
    readData = file.readlines()
    file.close()
    return readData

# defining function to store file contents in dictionary


def storeinDictionary(file):
    dictionary = {}
    for index in range(len(file)):
        dictionary[index +1] = file[index].replace("\n", "").replace(" ", "").split(",")
    return dictionary

# defining function to display available
def displayDictionary():
    contents = readEquipmentFile()
    equipment = storeinDictionary(contents)

    print("\n")
    print("ID", "|","Equipment Name", "\t|", "Manufacturer", "\t|",
          "Rental Price", "\t|", "Quantity Available", "\t|","Quantity Already Rented")
    print("______________________________________________________________________________________________________________")
    for key, value in equipment.items():
        print(key, " |", value[0], "\t\t", "|", value[1],
              "\t", "|", value[2], "\t", "|", value[3], "\t","\t\t|", value[4])

def displayProvidedDictionary(providedDictionary):
    print("\n")
    print("ID", "|","Equipment Name", "\t|", "Manufacturer", "\t|",
          "Rental Price", "\t|", "Quantity Available", "\t|","Quantity Already Rented")
    print("______________________________________________________________________________________________________________")
    for key, value in providedDictionary.items():
        print(key, " |", value[0], "\t\t", "|", value[1],
              "\t", "|", value[2], "\t", "|", value[3], "\t","\t\t|", value[4])