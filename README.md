# A random wheel generator that takes user inputs, records them in a list, then outputs one randomly selected input. 

# What the app does
1. program asks to create a wheel
2. program allows user to input options
3. user can keep adding options or write "done" to end option input
4. program outputs all added options
4. program asks user if they are ready to spin wheel, or restart options
5. if restart, delete current options list and go back to step 2
6. if ready to spin, program randomly selects one of the options
7. selected option is printed and then deleted from options list
8. program asks user if they would like to spin again
9. if yes, go back to step 6
10. if no, program asks if user would like to create a new wheel
11. if yes, go back to step 2
12. if no, end program

# How to run it
- def intro(): this function introduces the user to the wheel generator and allows them to choose to enter the program.
- def wheel(): this function takes user inputs, adds them to the options list to later be chosen from, and prints the entire options list when user is done inputting.
- def spin_wheel(): this function lets the user to choose to spin the wheel or restart inputting options. If the wheel is spun, it randomly selects an option from the list, prints it, then deletes it from the list.
- def final(): this function lets the user choose either to spin the current wheel again, create a new wheel with different options, or exit the program.