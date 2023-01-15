import MakeOrBreak.utils as utils

def main():
   interval = 0    
   valid = False

   while valid == False:
      print("Please set up your app.")
      print("Note that you will not be able to change your configurations later on")

      print("Difficulty Configuration:")
      print("Enter '1' for Hard mode")
      print("Enter '2' for Normal mode")
      print("Enter '2' for Easy mode")
      mode = int(input())

      if mode == 1:
         print("Hard Mode selected")
      if mode == 2:
         print("Normal Mode selected")
      if mode == 3:
         print("Easy Mode selected")


      print("Interval Configuration:")
      print("Enter '1' if you wish to recieve hourly reminders.")
      print("Enter '2' for a custom interval.")
      print("Enter '3' if you wish to recieve reminders randomly.")
      choice = int(input())

      # Hourly Reminders
      if choice == 1:
         interval = 3600
         valid = True
         print("App is now running on hourly intervals.")
      # Customer Reminders
      elif choice == 2:
         interval = input("Please Enter the custom Interval that you would like in seconds. ")
         interval = int(interval)
         valid = True
         print("App is now running on an interval of " + str(interval) + "s.")
      # Random intervals
      elif choice == 3:
         interval = 1
         valid = True
         print("App is now running on random intervals.")
      # Wrong choice
      else:
         print("Invalid choice! Please read carefully before choosing your choice again!")
         continue


   utils.runAsBackgroundProcess(mode, choice, interval)


if __name__ == "__main__":
   main()
