import rent
import datetime
import dictionary

def returnOneItem(equipments):
    dictionary.displayProvidedDictionary(equipments)
    returnProductId = rent.getProductIdFromUser()
    productNotRented = True
    
    item = None

    if returnProductId != 0:
        while productNotRented:
            if int(equipments[returnProductId][4]) == 0:
                print("\nThe product you chose has not been rented, kindly choose another one")
                returnProductId = rent.getProductIdFromUser()
                if returnProductId == 0:
                    productNotRented = False

            else:
                productNotRented = False
                returningQuantity = rent.getUserInputWithinBounds(1, int(equipments[returnProductId][4]), "No of items to be returned")
                if returningQuantity:
                    returningDays = rent.getUserInputWithinBounds(1, 365, "Return days")
                    if returningDays:
                        item = {"id":returnProductId, "quantity":returningQuantity, "date":datetime.datetime.now().strftime("%Y/%m/%d %I:%M:%S"), "returningDays": returningDays}
    return item


def writeToBill(customerDetails,equipments, cart):
    finePercentage = 20
    totalFine = 0
    returnDate = datetime.datetime.now()
    formattedReturnDate = returnDate.strftime("%Y/%m/%d %I:%M:%S")
    billFileName = customerDetails["email"]+"_"+formattedReturnDate.replace("/", "").replace(":", "").replace(" ", "_") + "_return.txt"

    bill = open(billFileName, "w")
    bill.write("Customer name: " + customerDetails["name"] + "\n")
    bill.write("Phone number: " + str(customerDetails["phone"]) + "\n")
    bill.write("Email address: " + customerDetails["email"] + "\n")
    bill.write("------------------------------------------------------------------------ \n")
    bill.write("Return Items Detail:\n")
    for index in range(len(cart)):
        fine = 0
        equipmentID = int(cart[index]["id"])
        equimentQuantity = int(cart[index]["quantity"])
        returningDays = int(cart[index]["returningDays"])
        rentedDate = formattedReturnDate
        equipmentName = equipments[equipmentID][0]
        equipmentMfg = equipments[equipmentID][1]
        rentalPrice = equipments[equipmentID][2]
        extraDays = int(returningDays) - 5
        
        if int(returningDays) > 5:
            fine = int(rentalPrice.replace("$","")) * finePercentage / 100 * extraDays * equimentQuantity
        
        totalFine = totalFine + fine
        
        print("\nEquipment ID: ", equipmentID)
        print("Equipment Name: ", equipmentName)
        print("Return Quantity: ", equimentQuantity)
        print("Returned after: " + str(returningDays) + " days")
        print("Equipment Manufacturer: ", equipmentMfg)
        print("Rental Price: ", rentalPrice)
        print("Return Date ", returnDate)
        if extraDays>0:
            print("Fine: $"+ str(fine) + " for returning item " + str(extraDays) + " day late")
            print("( Calculated as: " + str(finePercentage) + "% of "+str(rentalPrice)+" for each late day after 5 days of renting for each item)\n")
                
        bill.write("Equipment ID: " + str(equipmentID) + "\n")
        bill.write("Equipment Name: " + str(equipmentName) + "\n")
        bill.write("Return Quantity: " + str(equimentQuantity) + "\n")
        bill.write("Returned after: " + str(returningDays) + " days\n")
        bill.write("Equipment Manufacturer: " + str(equipmentMfg) + "\n")
        bill.write("Rental Price: " + str(rentalPrice) + "\n")
        bill.write("Return Date: " + str(rentedDate) + "\n")
        if extraDays>0:
            bill.write("Fine: $"+ str(fine) + " for returning item " + str(extraDays) + " day late\n")
            bill.write("( Calculated as: " + str(finePercentage) + "% of "+str(rentalPrice)+" for each late day after 5 days of renting for each item)\n")
        bill.write("\n")

        
    bill.write("------------------------------------------------------------------------ \n")
    bill.write("Return Summary:\n")
    bill.write("Total Fine: $" + str(totalFine))
    print("Total Fine: $" + str(totalFine))
    print("\n")
    
    bill.close()


def updatedEquipment(equipments, item):
    rentedItemInDictionary = equipments[item["id"]]

    #this is the number of items in stock 
    rentedItemInDictionary[3] = str(int(rentedItemInDictionary[3]) + int(item["quantity"]))

    # this is the number of items already rented, hence addition of the rented quantity
    rentedItemInDictionary[4] = str(int(rentedItemInDictionary[4]) - int(item["quantity"]))

    equipments[item["id"]] = rentedItemInDictionary
    
    return equipments
    
def salesReturn():
    returnCart = []
    fileContents = dictionary.readEquipmentFile()
    equipments = dictionary.storeinDictionary(fileContents)
    
    continueReturningProcess = True

    while continueReturningProcess:

        if len(returnCart) == 0:
            print("\n")
            print("--------------------------------------------------------------------")
            print("                            Return                                  ")
            print("--------------------------------------------------------------------")
            print("\n")
            print("Here is a list of the equipments, choose one to return:")

            returnedItem = returnOneItem(equipments)
            if returnedItem != None:
                returnCart.append(returnedItem)
                equipments = updatedEquipment(equipments, returnedItem)
            else:
                continueReturningProcess = False
        else:
            noOfItemsInCart = len(returnCart)
            print("\nINFO: "+str(noOfItemsInCart)+ " item ready to be returned")
            print('''\nSelect an option to continue:
                    (1) || Proceed to return.
                    (2) || Add another item to return.
                    (3) || Clear return cart''')
            checkoutDecision = rent.getUserInputWithinBounds(1, 3, "decision")

            if checkoutDecision != 0:
                if checkoutDecision == 1:
                    continueReturningProcess = False
                    customerDetails = rent.getCustomerDetails()
                    writeToBill(customerDetails, equipments, returnCart)
                    rent.updateEquipmentsFile(equipments)

                elif checkoutDecision == 2:        
                    returnedItem = returnOneItem(equipments)
                    if returnedItem != None:
                        equipments = updatedEquipment(equipments, returnedItem)
                        returnCart.append(returnedItem)

                elif checkoutDecision == 3:
                    returnCart.clear()
                    equipments = dictionary.storeinDictionary(fileContents)
                    continueReturningProcess = True
            else:
                continueReturningProcess = False