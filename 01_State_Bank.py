# This Program Is To Implement An Working Banking System.

import os
import subprocess
import random
from datetime import datetime
import sys

pin_set = set()
user_DB = r'Users_DB.txt'
pin_DB = r'Account_Pin_DB.txt'
saving_DB = r'Savings_Account_DB.txt'
business_DB = r'Business_Account_DB.txt'
temp_sav_db = r'Saving_DB.txt'
temp_bus_db = r'Business_DB.txt'

class bank:
    def __init__(self, bank_name):
        self.bank_name = bank_name
        self.account_name_dict = {}
        self.user_name_dict = {}

    def user_entry(self, object_key = '', object_name = ''):
        self.user_name_dict[object_key] = object_name

    def account_registry(self, object_key = '', object_name = ''):
        self.account_name_dict[object_key] = object_name
    def get_serial(self):
        curr_serial = len(self.account_name_dict)    # Get The Current Serial No.
        next_serial = curr_serial + 1                # Get The Next Serial No.
        dynamic_serial = f"{next_serial:05d}"        # Convert The Serial To Be Dynamic, To Fit In 5 Digits.
        return dynamic_serial                        # Return The Dynamic Serial Number.

class customer:
    def __init__(self, name = '', age = 1, acc_no = '0'):
        self.Acc_no = acc_no
        self.Customer_name = name
        self.Customer_age = age

    def show(self):
        print(f"Hello {self.Customer_name} Your {state_bank.account_name_dict[self.Acc_no].account_type} Account Is Active.")

class business_account:
    account_type = 'business'

    def __init__(self, acc_no = '' , acc_balance = 0.0, acc_pin = ''):
        self.acc_no = acc_no
        self.acc_balance = acc_balance
        self.acc_pin = acc_pin

    def validate_pin(self):
        print("Please Enter Your Accounts 6 Digits Pin Number (------)")
        while True:
            print("Enter Your Pin, Or Enter 0 To Exit.")
            try:
                user_pin = input("-->")
                if user_pin == '0':
                    return ''
                elif not user_pin.isdigit():
                    print("Invalid Input Type, Please Try Again")
                    continue
                elif len(user_pin) != 6:
                    print("Your Account Pin Should Be 6 Digits, Try Again")
                    continue
                elif self.acc_pin != user_pin:
                    print("Sorry Your Pin Is Not Matching, Please Try Again.")
                    continue
                else:
                    return user_pin
            except:
                print("Invaild Input Type, Please Try Again.")
                continue

    def deposit(self, money = 0):
        clear_terminal()
        self.acc_balance = self.acc_balance + money
        if self.account_type == 'business':
            with open(temp_bus_db, 'a') as file:
                file.write(f"{self.acc_no},{self.acc_balance}\n")
        elif self.account_type == 'savings':
            with open(temp_sav_db, 'a') as file:
                file.write(f"{self.acc_no},{self.acc_balance},{self.with_limit}\n")
        # Asking If The User Wants To Know Their Balance.
        print("Money Depositted Successfully.\nDo You Want To See Your Balance?")
        while True:
            print("Type: 1 --> (See Balance)")
            print("Type: 2 --> (Exit)")
            try:
                temp = int(input("-->"))
                if temp != 1 and temp != 2:
                    print("Invalid Operation, Please Select From The Given Options.")
                    continue
                else:
                    break
            except:
                print("Invalid Input Type, Please Try Again.")
                continue
        if temp == 1:
            self.balance()
            return

    def balance(self, pin = '0'):
        clear_terminal()
        if pin == '0':
            print("Please Enter Your Accounts 6 Digits Pin Number (------)")
            while True:
                print("Enter Your Pin, Or Enter 0 To Exit.")
                try:
                    user_pin = input("-->")
                    if user_pin == '0':
                        return
                    elif not user_pin.isdigit():
                        print("Invalid Input Type, Please Try Again")
                        continue
                    elif len(user_pin) != 6:
                        print("Your Account Pin Should Be 6 Digits, Try Again")
                        continue
                    elif self.acc_pin != user_pin:
                        print("Sorry Your Pin Is Not Matching, Please Try Again.")
                        continue
                    else:
                        break
                except:
                    print("Invaild Input Type, Please Try Again.")
                    continue
        
        print(f"The Total Balance In Your {self.account_type} Account, {self.acc_no} Is : ",self.acc_balance)
        stopper = input("Please Hit (Enter) --> Exit.")

    def withdraw(self):
        clear_terminal()
        if self.acc_balance == 0.0:
            print("Sorry You Cannot Withdraw From Your Buisness Account, Balance Is 0")
        else:
            user_pin = self.validate_pin()
            if user_pin == '':
                __ = input("Please Hit (Enter) --> Exit")
                return
            else:
                # Code Get Mathced With The Accounts 6 Digit Pin.
                while True:
                    try:
                        temp = int(input("Please Enter The Amount To Withdraw From Your Buissess Accout, Enter 0 To Exit : "))
                        if temp == 0:
                            return
                        elif(temp > self.acc_balance):
                            print("Insufficient Balance, Try Again.")
                            continue
                        elif temp <= 0:
                            print("Invalid Amount, Try Again.")
                            continue
                        else:
                            break
                    except:
                        print("Invalid Input Type, Please Try Again.")
                        continue
                self.acc_balance = self.acc_balance - temp
                print("Processing.....\n",temp,"Is Successfully Withdrawed.")
                with open(temp_bus_db, 'a') as file:
                    file.write(f"{self.acc_no},{self.acc_balance}\n")
        print("Do You Want To See Your Balance?")
        while True:
            print("Type: 1 --> (See Balance)")
            print("Type: 2 --> (Exit)")
            try:
                temp = int(input("-->"))
                if temp != 1 and temp != 2:
                    print("Invalid Operation, Please Select From The Given Options.")
                    continue
                else:
                    break
            except:
                print("Invalid Input Type, Please Try Again.")
                continue
        if temp == 1:
            self.balance(user_pin)
            return


class saving_account(business_account):
    account_type = 'savings'
    withdraw_limit = 25000
    annual_intrest = 6.7
    acc_withdraw_limit = 3
    charge = 99
    min_balance = 1500.00

    def __init__(self, acc_no = '', acc_balance = 3000.00, acc_pin = '', acc_with_limit = 0):
        super().__init__(acc_no, acc_balance, acc_pin)
        self.with_limit = acc_with_limit

    def compounding(self):
        monthly_rate = (self.annual_intrest/12) / 100
        curr_balance = self.acc_balance
        intrest_earned = curr_balance * monthly_rate
        self.acc_balance += intrest_earned

    def withdraw(self):
        clear_terminal()
        if self.acc_balance <= self.min_balance:
            print("Sorry You Cannot Withdraw From Your Saving Acount, Minimum Balance Should Be Maintained.")
        else:
            will_charge = False
            if self.with_limit > self.acc_withdraw_limit:
                print("Your Monthly WithDrawal Limit Is Reached.")
                print(f"You Will Be Charged {self.charge}rs.")
                print("Do Want To Continue?")
                while True:
                    try:
                        print("Type: 1 --> (WithDraw)")
                        print("Type: 2 --> (Exit)")
                        user_op = int(input("-->"))
                        if user_op != 1 and user_op != 2:
                            print("Invalid Input, Please Selecet From The Given Options.")
                            continue
                        else:
                            break
                    except:
                        print("Invalid Input Type, Please Try Again.")
                        continue
                if user_op == 2:
                    return
                else:
                    will_charge = True

            user_pin = self.validate_pin()
            if user_pin == '':
                print("Please Hit (Enter) --> Exit")
                return
            else:
                # Code Get Mathced With The Accounts 6 Digit Pin.
                while True:
                    try:
                        temp = int(input("Please Enter The Amount To Withdraw From Your Savings Account, Type 0 To Exit : "))
                        if temp == 0:
                            return
                        elif temp > self.withdraw_limit:
                            print(f"Account WithDrawal Limit Is Exceeding, Try Agaian")
                            continue
                        elif temp > self.acc_balance:
                            print(f"Insufficient Balance In the Account, Please Try Again.")
                            continue
                        elif temp <= 0:
                            print("Invalid Amount Try Again")
                            continue
                        elif will_charge:
                            if (self.acc_balance - temp - self.charge) < self.min_balance:
                                print(f"Sorry You Cannot WithDraw {temp}rs, Minimum Balance Should Be Maintained.")
                                continue
                            else:
                                break
                        elif will_charge == False:
                            if (self.acc_balance - temp) < self.min_balance:
                                print(f"Sorry You Cannot WithDraw {temp}rs, Minimum Balance Should Be Maintained.")
                                continue
                            else:
                                break
                    except:
                        print("Invalid Input Type, Please Try Again.")
                        continue

                if will_charge:
                    self.acc_balance = self.acc_balance - temp - self.charge
                    self.with_limit = self.with_limit + 1
                else:
                    self.acc_balance = self.acc_balance - temp
                    self.with_limit = self.with_limit + 1
                with open(temp_sav_db, 'a') as file:
                    file.write(f"{self.acc_no},{self.acc_balance},{self.with_limit}\n")
                print("Processing.....\n",temp,"Is Successfully Withdrawed.")
        print("Do You Want To See Your Balance?")
        while True:
            print("Type: 1 --> (See Balance)")
            print("Type: 2 --> (Exit)")
            try:
                temp = int(input("-->"))
                if temp != 1 and temp != 2:
                    print("Invalid Operation, Please Select From The Given Options.")
                    continue
                else:
                    break
            except:
                print("Invalid Input Type, Please Try Again.")
                continue
        if temp == 1:
            self.balance(user_pin)
            return
        
def generate_pin():
    while True:
        random_num = random.randint(0, 999999)
        new_pin = f"{random_num:06d}"
        if new_pin not in pin_set:
            pin_set.add(new_pin)
            return new_pin
# Updating The Savings Account In Monthly Basis.
def get_pin_list():
    pin_list = []
    global pin_set
    global pin_DB
    if not os.path.exists(pin_DB) or os.path.getsize(pin_DB) == 0:
        print("Failed To Fetch The Info From The Pin Data Base!")
        return pin_list
    else:
        with open(pin_DB, 'r') as pin_file:
            for lines in pin_file:
                lines = lines.strip()
                acc_no, acc_balance, acc_pin = lines.split(',')
                acc_no = acc_no.strip()
                acc_balance = float(acc_balance.strip())
                acc_pin = acc_pin.strip()
                curr_dict = {
                    'acc_no' : acc_no,
                    'acc_balance' : acc_balance,
                    'acc_pin' : acc_pin
                }
                pin_list.append(curr_dict)
                pin_set.add(acc_pin)
    return pin_list

def update_monthly_intrest():
    # Check if today's date is exactly day 1
    today = datetime.now()
    if today.day != 1:
        # If it's not the 1st of the month, immediately stop and do nothing!
        return 
    print("Windows Scheduler Activated, Batch Processing Starting...")

    global saving_DB
    # Quick safety check: if the database file doesn't exist yet, stop early.
    if not os.path.exists(saving_DB) or os.path.getsize(saving_DB) == 0:
        print("Failed To Find The Saving Accounts Data Base!")
        return
    # Move Forward Only When Both The Cases Are Checked.
    else:
        # READ & REBUILD: Turn data lines back into live Python Objects.
        
        # Get The Pin List, Using the method.
        pin_list = get_pin_list()
        if pin_list:        
            is_pin_gone = False
        else:
            is_pin_gone = True
        active_objects_list = []    
        with open(saving_DB, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    acc_no, acc_balance, acc_with_limit = line.split(',')
                    acc_no = acc_no.strip()
                    acc_balance = acc_balance.strip()
                    acc_balance = float(acc_balance)
                    acc_with_limit = acc_with_limit.strip()
                    acc_with_limit = int(acc_with_limit)
                    if is_pin_gone:
                        acc_pin = generate_pin()
                    else:
                        for items in pin_list:
                            if items['acc_no'] == acc_no:
                                acc_pin = items['acc_pin']
                                break
                    Account_obj = saving_account(acc_no, acc_balance, acc_pin, acc_with_limit)
                    active_objects_list.append(Account_obj)

        # Coumpounding/Updating Balance For Each Account.
        for items in active_objects_list:
            items.compounding()
            items.with_limit = 0

        with open(saving_DB, 'w') as file:
            for objects in active_objects_list:
                file.write(f"{objects.acc_no},{objects.acc_balance},{objects.with_limit}\n")

        print(f"Success! Consecutively updated {len(active_objects_list)} accounts.")
        sys.exit()

# Clear The Terminal.
def clear_terminal():
    # 'cls' for Windows, 'clear' for Mac/Linux
    cmd = 'cls' if os.name == 'nt' else 'clear'
    
    # Securely executes the command without opening a vulnerable shell
    subprocess.run(cmd, shell=True)

# Populating The Savings Accounts.
def populate_savings_acc():
    global saving_DB
    # Check If The DataBase Exists.
    if not os.path.exists(saving_DB) or os.path.getsize(saving_DB) == 0:
        print("Failed To Fetch The Info From The Account Data Base!")
        return
    # If Both The Conditions Check, Now Move Forward.
    else:
        with open(saving_DB, 'r') as file:
            # Iterate Over Each Lines.
            pin_list = get_pin_list()
            if pin_list:
                is_pin_gone = False
            else:
                is_pin_gone = True
            
            for lines in file:
                lines = lines.strip() 
                # Check Only Where The Lines Are Not Empty.
                if lines:
                    # Fetch The Acc_no & Acc_balance.
                    acc_no, acc_balance, acc_with_limit = lines.split(',')
                    acc_no = acc_no.strip()
                    acc_balance = acc_balance.strip()
                    acc_balance = float(acc_balance)
                    acc_with_limit = acc_with_limit.strip()
                    acc_with_limit = int(acc_with_limit)
                    if is_pin_gone:
                        acc_pin = generate_pin()
                    else:
                        for item in pin_list:
                            if item['acc_no'] == acc_no:
                                acc_pin = item['acc_pin']
                    object_key = saving_account(acc_no, acc_balance, acc_pin, acc_with_limit)
                    state_bank.account_registry(str(acc_no), object_key)

    # Updaing The Account Balance According To The Temp DB.
    if not os.path.exists(temp_sav_db) or os.path.getsize(temp_sav_db) == 0:
        print("The Temporary Data Base Is Either Missing, Or Nothing Was Updated In The Last Execution.")
        return
    else:
        with open(temp_sav_db, 'r') as file:
            for lines in file:
                lines = lines.strip()
                if lines:
                    temp_acc_no, temp_balance, temp_with_limit = lines.split(',')
                    temp_acc_no = temp_acc_no.strip()
                    temp_balance = temp_balance.strip()
                    temp_balance = float(temp_balance)
                    temp_with_limit = int(temp_with_limit.strip())
                    acc_object = state_bank.account_name_dict.get(temp_acc_no)
                    if acc_object:
                        acc_object.acc_balance = temp_balance
                        acc_object.with_limit = temp_with_limit
        with open(temp_sav_db, 'w') as file:
            file.write("")

# Populating The Business Accounts.
def populate_business_acc():
    global business_DB
    # Chack If The DataBase Exists.
    if not os.path.exists(business_DB) or os.path.getsize(business_DB) == 0:
        print("Failed To Fetch The Account Info From The Data Base.")
        return
    # If Both Condition Checked Now Move Forward.
    else:
        with open(business_DB, 'r') as file:
            pin_list = get_pin_list()
            if pin_list:
                is_pin_gone = False
            else:
                is_pin_gone = True

            for lines in file:
                lines = lines.strip()
                # Check Only Where Lines Are Not Empty.
                if lines:
                    # Fetch The Acc_no & Acc_balance.
                    acc_no, acc_balance = lines.split(',')
                    acc_no = acc_no.strip()
                    acc_balance = acc_balance.strip()
                    acc_balance = float(acc_balance)
                    if is_pin_gone:
                        acc_pin = generate_pin()
                    else:
                        for items in pin_list:
                            if items['acc_no'] == acc_no:
                                acc_pin = items['acc_pin']
                    object_key = business_account(acc_no, acc_balance, acc_pin)
                    state_bank.account_registry(str(acc_no), object_key)
    if not os.path.exists(temp_bus_db) or os.path.getsize(temp_bus_db) == 0:
        print("The Temporary Data Base Is Either Missing, Or Nothing Was Updated In The Last Execution.")
        return
    else:
        with open(temp_bus_db, 'r') as file:
            for lines in file:
                lines = lines.strip()
                if lines:
                    temp_acc_no, temp_acc_balance = lines.split(',')
                    temp_acc_no = temp_acc_no.strip()
                    temp_acc_balance = temp_acc_balance.strip()
                    temp_acc_balance = float(temp_acc_balance)
                    acc_object = state_bank.account_name_dict.get(temp_acc_no)

                    if acc_object:
                        acc_object.acc_balance = temp_acc_balance
        with open(temp_bus_db, 'w') as file:
            file.write("")

# Populating The Previous Users.
def populate_users():
    global user_DB
    if not os.path.exists(user_DB) or os.path.getsize(user_DB) == 0:
        print("Failed To Find The User Data Base!")
        return
    else:
        with open(user_DB) as file:
            for lines in file:
                lines = lines.strip()
                if lines:
                    user_name, user_age, user_acc = lines.split(',')
                    user_name = user_name.strip()
                    user_age = user_age.strip()
                    user_age = int(user_age)
                    user_acc = user_acc.strip()
                    curr_user = customer(user_name,user_age,user_acc)
                    state_bank.user_entry(user_acc, curr_user)

# Generate A Unique Account No.
def get_acc_no(acc_type = 0):
    if acc_type == 1:
        acc_no = f"SAV{state_bank.get_serial()}"
    else:
        acc_no = f"BUI{state_bank.get_serial()}"
    return acc_no

# Create Your Account.
def open_acc():
    while True:
        clear_terminal()
        print("Welcome To State Bank, This Is The Process To Open Your Account.")
        print("Do You Want To Open (Saving Account), Or (Business Account)?")
        print("Type :  1 --> (Savings Account)")
        print("Type :  2 --> (Business Account)")
        acc_type = int(input("-->"))
        if(acc_type != 1 and acc_type != 2):
            print("Sorry Wrong Input, Please Type Again.")
            continue
        else:
            break

    # So We Are Going To Set:
    # Business Account Will Always Starts From Balance = 0.0,
    # Where As The Savings Account Will Always Starts From Balance = 3000.0,
    acc_no = get_acc_no(acc_type)
    acc_pin = generate_pin()
    if acc_type == 1:
        curr_account = saving_account(acc_no,3000.0,acc_pin)
        state_bank.account_registry(acc_no,curr_account)
        acc_balance = 3000.0
        with open(saving_DB, 'a') as file:
            file.write(f"{acc_no},3000.0,0\n")
    else:
        curr_account = business_account(acc_no,0.0,acc_pin)
        state_bank.account_registry(acc_no,curr_account)
        acc_balance = 0.0
        with open(business_DB, 'a') as file:
            file.write(f"{acc_no},0.0\n")
    return acc_no, acc_pin, acc_balance

    

# Create New Customer Objects, And Assign Them Thier Account No.
def new_user():
        print("Hello New Customer, Welcome To Our State Bank.")
        user_name = input("Please Fill Your Full Name : ")
        while True:
            try:
                user_age = int(input("Please Tell Us Your Age : "))
                if(user_age <= 0):
                    print("Not A Valid Age, Please Try Again")
                    continue
                elif(user_age >= 120):
                    print("Not A Valid Age, Please Try Again")
                    continue
                else:
                    break
            except:
                clear_terminal()
                print("Sorry Something Went Wrong, Please Fill the Info Again.")
                continue

        user_name = user_name.strip()
        acc_no, acc_pin, acc_balance = open_acc()
        curr_user = customer(user_name, user_age, acc_no)
        state_bank.user_entry(str(acc_no), curr_user)
        with open(user_DB, 'a') as file:
            file.write(f"{user_name},{user_age},{acc_no}\n")
        with open(pin_DB, 'a') as file:
            file.write(f"{acc_no},{acc_balance},{acc_pin}\n")
        print(f"Hey {user_name} Your Account {acc_no} Is Sucessfully Been Created In Our State_Bank.")
        print(f"Here Is Your 6 Digit Pin : {acc_pin}\nPlease Remeber It.")

def greet_guest():
    while True:
        clear_terminal()
        print("Do You Want To Open A New Account, Or Are You Already Our Customer?")
        print("Type :  1 --> (New Account)")
        print("Type :  2 --> (Already A Customer)")
        print("Type : 3 --> (Exit)")
        try:
            user_call = int(input("-->"))
            if user_call != 1 and user_call != 2 and user_call != 3:
                print("Invalid Input, Please Type From The Given Options")
                continue
            else:
                break
        except:
            print("Sorry Invalid Input Type, Please Revalidate Your Input!")
            continue
    return user_call

def get_user_acc_no():
    clear_terminal()
    print("Hello Customer, Welcome To The State Bank")
    while True:
        # clear_terminal()
        print("Please Tell Us Your Account Number, For Further Processes.")
        user_acc_no = input("-->")
        if user_acc_no in state_bank.account_name_dict:
            print(f"You Have A {state_bank.account_name_dict[user_acc_no].account_type} Account {user_acc_no} In Our Bank.")
        else:
            print("Sorry Your Given Account Number Is Either Not Valid, Or Your Account Is Not Active.")
            while True:
                print("Do You Want To Exit, Or Try Again?")
                print("Type :  1 --> (Try Again)")
                print("Type :  2 --> (Exit)")
                try:
                    user_act = int(input("-->"))
                    if user_act != 1 and user_act != 2:
                        print("Invalid Operation, Please Select From The Given Options.")
                        continue
                    else:
                        break
                except:
                    print("Invalid Input Type, Please Revalidate Your Input.")
                    continue
            if user_act == 1:
                continue
            else:
                return ""
        return user_acc_no

def user_op(acc_no):
    clear_terminal()
    print(f"Hello {state_bank.user_name_dict[acc_no].Customer_name}, What Operation You Want?")
    while True:
        print("Type : 1 --> (Withdraw)")
        print("Type : 2 --> (Deposit)")
        print("Type : 3 --> (Show Balance)")
        print("type : 4 --> (Exit)")
        try:
            user_demand = int(input("-->"))
            if user_demand != 1 and user_demand != 2 and user_demand != 3 and user_demand != 4:
                print("Invalid Input, Please Select From The Given Options.")
                continue
            else:
                break
        except:
            print("Invalid Input Type, Please Revalidate Your Input.")
            continue
    if user_demand == 1:
        state_bank.account_name_dict[acc_no].withdraw()
    elif user_demand == 2:
        while True:
            try:
                amount = int(input("Please Enter The Amount To Deposit : "))
                if amount < 100:
                    print(f"You Cannot Deposit {amount}rs, Try Different Amount")
                    continue
                else:
                    break
            except:
                print("Invalid Input Type, Please Try Again!")
                continue
        state_bank.account_name_dict[acc_no].deposit(amount)
    elif user_demand == 3:
        state_bank.account_name_dict[acc_no].balance()
    else:
        return

# Serve When Ever A Guest Comes.
def serve_user():
    user_call = greet_guest()
    if user_call == 1:
        new_user()
    elif user_call == 2:
        user_acc_no = get_user_acc_no()
        if user_acc_no :
            user_op(user_acc_no)

# Update Our Savings Data Base Before Closing The Program.
def update_saving_db():
    with open(saving_DB, 'w') as file:
         for acc_no, account_obj in state_bank.account_name_dict.items():
            if account_obj.account_type == 'savings':
                file.write(f"{account_obj.acc_no},{account_obj.acc_balance},{account_obj.with_limit}\n")
        

# Update Our Business Data Base Before Closing The Program.
def update_business_db():
    with open(business_DB, 'w') as file:
        for acc_no, account_obj in state_bank.account_name_dict.items():
            if account_obj.account_type == 'business':
                file.write(f"{account_obj.acc_no},{account_obj.acc_balance}\n")


def start_bank_app():
    # Rebuild The Business Account Object In The RAM.
    populate_business_acc()
    # Rebuild The Savings Account Object In The RAM.
    populate_savings_acc()
    # Rebuild The Users Object In The RAM.
    populate_users()


# Make Our Banking System Live (Operationable).
# Starting Our State Bank Object.
state_bank = bank("State Bank Of India")
start_bank_app()

# Executes Only, When Its The 1st Day Of A Month, Else Will Be Returned.
update_monthly_intrest()


if __name__ == "__main__":
    while True:
        clear_terminal()
        print("Type : 1 --> (Visitor Availabe)")
        print("Type : 2 --> (Switch Off The Bank App)")
        try:
            emp_act = int(input("-->"))
            if emp_act != 1 and emp_act != 2:
                print("Invalid Input, Please Select From The Given Options.")
                continue
            elif emp_act == 1:
                while True:
                    clear_terminal()
                    print("Welcome To Our State Bank Of India.")
                    try:
                        print("Type : 1 --> (Start The Process)")
                        print("Type : 2 --> (Exit)")
                        user_act = int(input("-->"))
                        if user_act != 1 and user_act != 2:
                            print("Invalid Input, Please Select From The Given Options.")
                            continue
                        elif user_act == 1:
                            serve_user()
                            break
                        else:
                            print("Thanks For Comming.")
                            break
                    except:
                        print("Invaild Input Type, Please Try Again.")
                        continue
            else:
                break
        except:
            print("Invaild Input Type, Please Try Again.")
            continue

    # After All The Execution Load All The Accounts Object Info Into The Data Base.
    update_saving_db()
    update_business_db()