import sys
import rent
import salesReturn

# importing datetime function and sys module


def welcome():

    userContinues = True
    while userContinues:
        print("             -----------------------------------             ")
        print("             Welcome to Equipment Rental System!             ")
        print("             -----------------------------------             ")
        print('''Select an option to continue:
                    (1) || Input 1 to RENT an equipment.
                    (2) || Input 2 to RETURN an equipment.
                    (0) || Input 3 to EXIT.''')

        userInput = rent.getUserInputWithinBounds(0, 2,"decision")

        if userInput == 0:
            print("Thank you for using our system.!")
            sys.exit()
        elif userInput == 1:
            rent.rent()
        elif userInput == 2:
            salesReturn.salesReturn()

welcome()
