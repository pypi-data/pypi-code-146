from MakeOrBreak.utils import runAsBackgroundProcess

def main():
   interval = 0    
   valid = False

   while valid == False:
      print("Please set up your app.")
      print("Enter '1' if you wish to recieve hourly reminders.")
      print("Enter '2' for a custom interval.")
      print("Enter '3' if you wish to recieve reminders randomly.")
      choice = int(input())

      # Hourly Reminders
      if choice == 1:
         interval = 3600
         valid = True
         print("App is now running with hourly reminders.")
         # timer(choice, interval) 
      # Customer Reminders
      elif choice == 2:
         interval = input("Please Enter the custom Interval that you would like in seconds. ")
         interval = int(interval)
         valid = True
         print("App is now running with reminders every " + str(interval) + "s.")
         # timer(choice, interval)
      # Random intervals
      elif choice == 3:
         interval = 1
         valid = True
         # print("Update Success! App is now running on random intervals.")
         print("App is now running..")
         # timer(choice, interval)
      # Wrong choice
      else:
         print("Invalid choice! Please read carefully before choosing your choice again!")

   runAsBackgroundProcess(choice, interval)


if __name__ == "__main__":
   main()
