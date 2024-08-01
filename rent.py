import dictionary
import datetime


def getUserInputWithinBounds(lower, upper, name):
    validInput = False
    valueError = False
    userInput = -1
    while not validInput:

        valueError = False
        try:
            userInput = int(input("\nEnter " + name +
                                  " between " + str(lower) + " and "+str(upper) + " or ( 0 to discountinue) : "))
        except ValueError:
            valueError = True

        if (valueError):
            print("\nInvalid input, please enter a number")
        elif (userInput == 0):
            validInput = True
        elif (userInput < lower):
            print("\n"+name + " must be greater than or equals to " + str(lower))
        elif (userInput > upper):
            print("\n"+name + " must be less than or equals to " + str(upper))
        else:
            validInput = True
    return userInput


def getProductIdFromUser():
    fileContents = dictionary.readEquipmentFile()
    equipments = dictionary.storeinDictionary(fileContents)
    return getUserInputWithinBounds(1, len(equipments), "Product Id")

def getQuantityFromUser(equipments, productId):
    return getUserInputWithinBounds(1, int(equipments[productId][3]), "Quantity")


def rentOneItem(equipments):
    dictionary.displayProvidedDictionary(equipments)
    rentingProductId = getProductIdFromUser()
    item = None
    productNotInStock = True

    if rentingProductId != 0:
        while productNotInStock:
            if int(equipments[rentingProductId][3]) == 0:
                print("\nThe product you chose is out of stock, kindly choose another one")
                rentingProductId = getProductIdFromUser()
                if rentingProductId == 0:
                    productNotInStock = False
            else:
                productNotInStock = False
                rentingProductQuantity = getQuantityFromUser(equipments, rentingProductId)
                if rentingProductQuantity != 0:
                    item = {"id":rentingProductId, "quantity":rentingProductQuantity, "date":datetime.datetime.now().strftime("%Y/%m/%d %I:%M:%S")}

    return item

def getCustomerDetails():
    customerName = input("Customer name: ")
    customerEmail = input("Email address: ")
    validPhone = False

    while not validPhone:
        try:
            customerPhone = int(input("Phone number: "))
            validPhone = True
        except ValueError:
            print("Please enter numerical value for the phone number")
            validPhone = False        

    return {"name": customerName, "phone": customerPhone, "email": customerEmail}

def writeToBill(customerDetails,equipments, cart):
    grandTotal = 0
    rentDate = datetime.datetime.now()
    formattedRentDate = rentDate.strftime("%Y/%m/%d %I:%M:%S")
    billFileName = customerDetails["email"]+"_"+formattedRentDate.replace("/", "").replace(":", "").replace(" ", "_") + "_rent.txt"

    bill = open(billFileName, "w")
    bill.write("Customer name: " + customerDetails["name"] + "\n")
    bill.write("Phone number: " + str(customerDetails["phone"]) + "\n")
    bill.write("Email address: " + customerDetails["email"] + "\n")
    bill.write("------------------------------------------------------------------------ \n")
    bill.write("Rented Items Detail:\n")
    for index in range(len(cart)):
        equipmentID = int(cart[index]["id"])
        equimentQuantity = int(cart[index]["quantity"])
        rentedDate = cart[index]["date"]
        equipmentName = equipments[equipmentID][0]
        equipmentMfg = equipments[equipmentID][1]
        rentalPricePerPiece = equipments[equipmentID][2]
        rentalPriceTotal = int(rentalPricePerPiece.replace("$", "")) * equimentQuantity

        print("\nEquipment ID: ", equipmentID)
        print("Equipment Name: ", equipmentName)
        print("Rented Quantity: ", equimentQuantity)
        print("Equipment Manufacturer: ", equipmentMfg)
        print("Rental Price (per piece): ", rentalPricePerPiece)
        print("Rented Date ", rentDate)
        print("Rental Total: $", rentalPriceTotal)
        print("\n")
                
        bill.write("Equipment ID: " + str(equipmentID) + "\n")
        bill.write("Equipment Name: " + str(equipmentName) + "\n")
        bill.write("Rented Quantity: " + str(equimentQuantity) + "\n")
        bill.write("Equipment Manufacturer: " + str(equipmentMfg) + "\n")
        bill.write("Rental Price (per piece): " + str(rentalPricePerPiece) + "\n")
        bill.write("Rented Date: " + str(rentedDate) + "\n")
        bill.write("Rental Total: $" + str(rentalPriceTotal)+ "\n")
        bill.write("\n")

        grandTotal = grandTotal + rentalPriceTotal
        
    bill.write("------------------------------------------------------------------------ \n")
    bill.write("Rent Summary:\n")
    bill.write("GrandTotal: $" + str(grandTotal))

    print("------------------------------------------------------------------------ \n")
    print("Rent Summary:\n")
    print("GrandTotal: $" + str(grandTotal))
    print("\n")

    bill.close()

def updatedEquipment(equipments, item):
    rentedItemInDictionary = equipments[item["id"]]

    #this is the number of items in stock 
    rentedItemInDictionary[3] = str(int(rentedItemInDictionary[3]) - int(item["quantity"]))

    # this is the number of items already rented, hence addition of the rented quantity
    rentedItemInDictionary[4] = str(int(rentedItemInDictionary[4]) + int(item["quantity"]))

    equipments[item["id"]] = rentedItemInDictionary
    
    return equipments

def updateEquipmentsFile(equipments):
    editStock = open("equipments.txt", "w")
    for value in equipments.values():
        line = value[0] + "," + value[1] + "," + value[2] + "," + value[3] + "," + value[4] + "\n"
        editStock.write(line)
    editStock.close()

def rent():
    cart = []
    fileContents = dictionary.readEquipmentFile()
    equipments = dictionary.storeinDictionary(fileContents)

    continueRentingProcess = True

    while continueRentingProcess:
        if len(cart) == 0:
            print("\n")
            print("--------------------------------------------------------------------")
            print("                            Rent                                    ")
            print("--------------------------------------------------------------------")
            print("\n")
            print("Here is a list of the equipments:")
            
            rentedItem = rentOneItem(equipments)
            if rentedItem != None:
                cart.append(rentedItem)
                equipments = updatedEquipment(equipments, rentedItem)
            else:
                continueRentingProcess = False
        else:
            noOfItemsInCart = len(cart)
            print("\nINFO: "+str(noOfItemsInCart)+ " item in cart")
            print('''\nSelect an option to continue:
                    (1) || Proceed to checkout.
                    (2) || Continue renting.
                    (3) || Clear cart''')
            checkoutDecision = getUserInputWithinBounds(1, 3, "decision")
        
            if checkoutDecision != 0:
                if checkoutDecision == 1:
                    continueRentingProcess = False
                    customerDetails = getCustomerDetails()
                    writeToBill(customerDetails, equipments, cart)
                    updateEquipmentsFile(equipments)

                elif checkoutDecision == 2:        
                    rentedItem = rentOneItem(equipments)
                    if rentedItem != None:
                        equipments = updatedEquipment(equipments, rentedItem)
                        cart.append(rentedItem)

                elif checkoutDecision == 3:
                    cart.clear()
                    equipments = dictionary.storeinDictionary(fileContents)
                    continueRentingProcess = True
            else: 
                continueRentingProcess = False