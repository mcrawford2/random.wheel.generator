"""Welcome to the Random Wheel Generator. This program allows you to create a wheel with various options and spin it to get random results. You can customize the wheel by adding your own options, and the program will randomly select one when you spin it."""

import random

def wheel():
    """Creates the wheel and takes user input for options"""
    
    print("Welcome to the Random Wheel Generator!")
    print("You can add options to your wheel and spin it to get a random result.")

    options = []
    while True:
        option = input("Enter option (or type 'done' to finish): ").strip() #.strip() removes any leading or trailing whitespace from the input
        
        if option == "": #for empty input, prompt the user to enter something
            print("Input cannot be empty. Please enter something.")
            continue
        
        if option.lower() == 'done': #case sentitivity, converts the input to lowercase and checks if it is 'done' to exit the loop
            break

        options.append(option) #adds input to the options list

    if not options: #checks if the options list is empty, if it is, it prints a message and exits the program
        print("Exiting the program.")
        return

    print("\nYour wheel has the following options:")
    for idx, opt in enumerate(options, 1):
        print(f"{idx}. {opt}")
#idx is the index number starting at 1, opt is the option from the options list. This loop prints each option with its corresponding number.

    input("\nPress Enter to spin the wheel...")
    result = random.choice(options)
    print(f"The wheel landed on: {result}")
#random.choice() function selecta a random option from the options list and prints the result.