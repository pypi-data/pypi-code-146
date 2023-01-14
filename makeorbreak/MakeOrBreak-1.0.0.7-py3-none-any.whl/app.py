from controller import timer


def Main():

    interval = 0
    
    choice = 9

    while choice != 1 or choice != 2 or choice != 3:
        choice = input("Please set up your app.\n" +
                        "Enter '1' if you wish to recieve hourly reminders.\n" +
                        "Enter '2' for a custom interval.\n" + 
                        "Enter '3' if you wish to recieve reminders randomly.\n")

        # Hourly Reminders
        if choice == 1:
            interval = 3600
        # Customer Reminders
        elif choice == 2:
            interval = input("Please Enter the custom Interval that you would like in seconds.")
        # Random intervals
        elif choice == 3:
            interval = 1
        # Wrong choice
        else :
            print("Invalid choice! Please read carefully before choosing your choice again!")

    timer(choice, interval)


    
if __name__ == "__main__":
    print("Running app.py")

