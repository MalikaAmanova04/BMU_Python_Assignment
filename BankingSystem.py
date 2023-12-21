# Function to check if the password is valid
def is_password_valid(username, password):
    # Check if password length is less than 8
    if len(password) < 8:
        print("Password should have more than 8 digits/letters")
        return False

    # Check if password has only lower case or only upper case letters
    has_lower = False
    has_upper = False
    for char in password:
        if char.islower():
            has_lower = True
        if char.isupper():
            has_upper = True

    if not has_lower or not has_upper:
        print("Password should include at least one lower case and one upper case letter")
        return False

    # Check if password has at least one digit
    has_digit = False
    for char in password:
        if char.isdigit():
            has_digit = True
            break

    if not has_digit:
        print("Password should include at least one number")
        return False

    # Check if password is the same as username
    if username == password:
        print("Password cannot be equal to the username")
        return False

    # If all checks are passed, return True
    return True


# Function to import data from a file and create a bank dictionary
def import_and_create_bank(filename):
    # Create an empty dictionary to store bank data
    bank = {}

    # Open the file for reading
    with open(filename, 'r') as file:
        # Process each line in the file
        for line in file:
            # Remove any leading/trailing whitespace from the line
            line = line.strip()

            # Check if the line is not empty
            if line:
                # Split the line into key (account name) and value (balance)
                key, value = line.split(':')

                # Try to convert the balance value to a floating-point number
                try:
                    value = float(value)
                    # If successful, add the account and balance to the bank dictionary
                    bank[key] = value
                except ValueError:
                    # If conversion fails, skip this line and continue with the next
                    continue

    # Return the populated bank dictionary
    return bank



# Function to import user accounts data from a file and create account dictionaries
def import_and_create_accounts(filename):
    # Create two empty dictionaries for user accounts and login statuses
    user_accounts = {}
    log_in = {}

    # Open the file for reading
    with open(filename, 'r') as file:
        # Process each line in the file
        for line in file:
            # Remove any leading/trailing whitespace from the line
            line = line.strip()

            # Check if the line is not empty
            if line:
                # Split the line into username and password
                parts = line.split('-')

                # Check if there are exactly two parts and the password is not empty
                if len(parts) == 2 and parts[1]:
                    username, password = parts

                    # Check if the password is valid
                    if is_password_valid(username, password):
                        # If valid, add the user to the user accounts dictionary and set login status to True
                        user_accounts[username.strip()] = password.strip()
                        log_in[username.strip()] = True
                    else:
                        # If invalid, set the user's login status to False
                        log_in[username.strip()] = False

    # Return the user accounts dictionary and login statuses
    return user_accounts, log_in


# Function to sign up a new user
def signup(user_accounts, log_in, username, password):
    # Check if the username already exists in the user accounts
    if username in user_accounts:
        print('Already Exists')
        return False
    else:
        # Validate the provided password
        valid = is_password_valid(username, password)

        # If the password is valid, add the user to the user accounts
        if valid:
            user_accounts[username] = password
            log_in[username] = False  # Set the initial login status to False
            print('Username is Created. Go and log in')
            return True
        else:
            # If the password is not valid, return False
            return False

        
        
# Function for user login
def login(user_accounts, log_in, username, password):
    # Check if the username exists in the user accounts
    if username in user_accounts:
        # Check if the provided password matches the stored password
        if password == user_accounts[username]:
            log_in[username] = True  # Update the login status to True
            print("You successfully logged in")
            return True
        else:
            # If the password doesn't match, inform the user
            print("Password is not correct")    
    else:
        # If the username doesn't exist, inform the user
        print(f"We couldn't find a user called '{username}'")
        return False


# Function to update the bank balance for a user
def update(bank, log_in, username, amount):
    # Check if the user is not already in the bank system
    if username not in bank:
        # If not, initialize their balance to 0
        bank[username] = 0

        # If the user exists, check if they are logged in
    if log_in[username]:
            # Get the current balance and convert it to a float for calculation
        balance = float(bank[username])

            # Add the specified amount to the current balance
        new_balance = balance + amount

            # Update the bank balance for the user
        bank[username] = new_balance

            # Inform the user that their balance was successfully updated
        print("Your balance has been updated successfully!")
        return True
    else:
            # If the user is not logged in, inform them
        print("Please log in to update your balance.")
    
    # Return False if the update was not successful
    return False

        
# Function to transfer money from one user to another
def transfer(bank, log_in, userA, userB, amount):
    # Check if the amount to be transferred is positive
    if amount > 0:
        pass  # Proceed if the amount is positive
    else:
        # Inform the user if the amount is negative
        print("Negative amounts cannot be transferred.")
        return False
    
    # Check if userA exists in the bank and is logged in
    if userA in bank and userA in log_in:
        # Check if userA is logged in and has enough balance
        if log_in[userA] and bank[userA] >= amount:
            # Deduct the amount from userA's account
            bank[userA] -= amount

            # Check if userB exists in the bank, create an account if not
            if userB not in bank:
                print(f"A new account for '{userB}' has been created.")
                bank[userB] = 0

            # Add the amount to userB's account
            bank[userB] += amount

            # Inform the user that the transaction was successful
            print("The transaction was completed successfully.")
            return True
        else:
            # Inform userA if they are not logged in or don't have enough balance
            if not log_in[userA]:
                print("Please log in to complete the transaction.")
            else:
                print("Insufficient balance for the transaction.")
    else:
        # If userA doesn't exist in the bank or is not logged in
        print("Transaction cannot be processed. User may not exist or is not logged in.")

    # Return False if the transaction was not successful
    return False



# Function to change the password for a user account
def change_password(user_accounts, log_in, username, old_password, new_password):
    # Check if the username exists in the user accounts
    if username in user_accounts:
        # Check if the user is logged in
        if log_in.get(username):
            # Check if the old password matches the current password
            if user_accounts[username] == old_password:
                # Check if the new password is different from the old password
                if new_password != old_password:
                    # Validate the new password
                    if is_password_valid(username, new_password):
                        # Update the user's password
                        user_accounts[username] = new_password
                        # Log the user out after password change
                        log_in[username] = False
                        # Inform the user that their password has been changed
                        print("Password has been successfully changed! Please log in with your new password.")
                        return True
                    else:
                        # Inform the user if the new password is not valid
                        print("The new password is not valid. Please choose a different password.")
                else:
                    # Inform the user if the new password is the same as the old password
                    print("The new password cannot be the same as the old password.")
            else:
                # Inform the user if the old password does not match the current password
                print("The old password does not match our records.")
        else:
            # Inform the user if they are not logged in
            print("You need to be logged in to change your password.")
    else:
        # Inform the user if the username does not exist
        print("Username not found.")

    # Return False if the password change was not successful
    return False

# Function to delete a user account
def delete_account(user_accounts, log_in, bank, username, password):
    # Check if the username exists in the user accounts
    if username in user_accounts:
        # Check if the provided password matches the stored password
        if user_accounts.get(username) == password:
            # Check if the user is currently logged in
            if log_in.get(username):
                # Delete the user from the user accounts
                del user_accounts[username]
                # Delete the user's login status
                del log_in[username]

                # If the user has a bank account, delete it as well
                if username in bank:
                    del bank[username]

                # Inform the user that their account has been deleted
                print("Your account has been deleted successfully.")
                return True
            else:
                # Inform the user if they are not logged in
                print("You need to be logged in to delete your account.")
        else:
            # Inform the user if the password does not match
            print("The password you entered is incorrect.")
    else:
        # Inform the user if the username does not exist
        print("Username not found.")

    # Return False if the account deletion was not successful
    return False



    
# Main function for the banking application
def main():
    # Import bank details and user accounts from files
    bank = import_and_create_bank('bank.txt')
    user_accounts, log_in = import_and_create_accounts('user.txt')

    # Welcome message
    print("Welcome to 'BMU' Bank! We are glad to see you here. Please choose an option to proceed.")

    # Main loop to handle user options
    while True:
        # Display the current bank and user details
        print("\nBank details: ", bank)
        print("User accounts details: ", user_accounts)
        print("Login details: ", log_in)

        # Menu options
        print("\n--- Menu ---")
        print("1 -> Login")
        print("2 -> Signup")
        print("3 -> Change Password")
        print("4 -> Delete Account")
        print("5 -> Update Balance")
        print("6 -> Transfer Money")
        print("7 -> Exit")

        # User input for choosing an option
        option = input("\nWhat would you like to do? Please enter a number: ")

        # Handle different options
        if option == "1":
            # Handle user login
            username = input("Please enter your username: ")
            password = input("Please enter your password: ")
            login(user_accounts, log_in, username, password)

        elif option == "2":
            # Handle user signup
            username = input("Please enter a new username: ")
            password = input("Please enter a new password: ")
            signup(user_accounts, log_in, username, password)

        elif option == "3":
            # Handle password change
            username = input("Enter your username: ")
            old_password = input("Enter your old password: ")
            new_password = input("Enter your new password: ")
            change_password(user_accounts, log_in, username, old_password, new_password)

        elif option == "4":
            # Handle account deletion
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            delete_account(user_accounts, log_in, bank, username, password)

        elif option == "5":
            # Handle balance update
            username = input("Enter your username: ")
            amount = float(input("Enter the amount to update: "))
            update(bank, log_in, username, amount)

        elif option == "6":
            # Handle money transfer
            userA = input("Enter your username: ")
            userB = input("Enter the recipient's username: ")
            amount = float(input("Enter the amount to transfer: "))
            transfer(bank, log_in, userA, userB, amount)

        elif option == "7":
            # Exit the program
            print("Thank you for using 'BMU' Bank. Have a great day!")
            break

        # Separator for readability
        print("\n--- End of Action ---\n")

# Check if this script is the main program and run it
if __name__ == '__main__':
    main()
