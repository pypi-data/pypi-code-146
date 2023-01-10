def run_steps():
    step = 1
    while step <= 10:
        print(f"Current step: {step}")
        entered_step = input("Please enter the number of the step: ")
        if entered_step != str(step):
            print("Incorrect step entered. Exiting...")
            break
        print(f"Proceeding to step {step+1}...")
        step += 1
    print("All steps completed!")
