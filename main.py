import getpass
from Transactions import generate_transaction_id
from clear import clear
from headline import *
from timers import timer
import hashlib
from database_operations import *

class Details:
    acc_id = None
    card_number = None
    DOB = None

    def __init__(self,a,c,d):
        self.acc_id = a
        self.card_number = c
        self.DOB = d

# To get general details of the user's account. 
D=None
C=None
amnt=0.00
msg=""

def convertTuple(tup):
    st = '\t'.join(map(str, tup))
    return st

def transaction_done(transaction_id,m,amnt):
    global D
    global msg
    if(D==None):
        D=Details("None","None","None")
        msg="Failed Transaction"
    try:
        C.addtransaction(transaction_id,D.acc_id,dt(),tym(),msg,amnt)
    except:
        print("\t\t Sorry for the inconvenience.\t\t Transaction Not Completed.")

def authenticate():
    clear()
    header()
    global msg
    card_number=input("Enter your card number : ")
    
    if(len(card_number)>12 or len(card_number)<12):
        print("Card Number must be of 12 Length.. Try Again..")
        return False
    elif(not card_number.isdigit()):
        print("Card Number should contain numbers only...")
        return False
    
    pin=getpass.getpass('PIN : ')
    
    if(len(pin)>4 or len(pin)<4):
        print("PIN must be of 4 Length.. Try Again..")
        return False
    elif(not pin.isdigit()):
        print("PIN should contain positive numbers only...")
        return False
    
    hashed=hashlib.md5(pin.encode()).hexdigest()
    global C
    try:
        dt=C.getdata(card_number)

        # print(type(dt))

        if(dt==None):
            print("Card Not found/Registered with the Bank...")
            msg="Transaction Failed."
            timer(1)
            return False

        p,a,c,d=dt
        global D
        D=Details(a,c,d)
    except :
        print("\t\t\t\t It's not you it's us. Sorry for the inconenience.")
        msg="Server Error"
        return False

    if (hashed==p):
        print("Connecting to Main Menu..")
        return True
    print("Wrong PIN Entered...")
    msg="Transaction Failed."
    return False
    
def menu():
    clear()
    header()
    print("\t\t\t1. EXIT \t\t\t 2. Balance Inquiry \t\t\t\n\t\t\t3. PIN Change \t\t\t 4. Cash Withdrawl")
    choice=input("Enter your choice : ")
    if(len(choice)>1 and not choice.isdigit()):
        choice='-1'
    return int(choice)

def balance():
    clear()
    try:
        balance=C.fetchbalance(D.acc_id)[0]
    except:
        print("\t\t\t\t It's not you it's us. Sorry for the inconenience.")

    header()
    print("\t\t\t\t Your Balance is: ",end="")
    print(balance)
    global msg
    # transaction_done(transaction_id)
    msg="Balance Checked"
    ans=input("\n\n\t\t\t Do you want to Print Mini Statement(Y/N)?:")
    if(len(ans)>1 and (not ans=='Y' or not ans=='N')):
        print("Please enter 'Y' or 'N' next tym only.")
    if ans=='Y':
        print("\n\n\t\t\tPrinting Mini Statement")
        timer(1)
        mini_statement()
    timer(1)   

def pin_change():
    clear()
    header()
    global msg
    dob=input("Enter your Date of Birth (YYYY-MM-DD) : ")
    result=validate(dob)
    if(not result):
        msg="Transaction Failed"
        print("Date of Birth should match this format->(YYYY-MM-DD) and it should contains digits only like '1990-01-21' ")
        timer(2)
        return False
    if(dob==D.DOB):
        p=getpass.getpass('Enter New PIN : ')
        if(not p.isdigit()):
            print("PIN should contain numbers only...")
            msg="Transaction Failed"
            timer(2)
            return False
        elif(len(p)>4 or len(p)<4):
            print("PIN must be of 4 Length.. Try Again..")
            msg="Transaction Failed"
            timer(2)
            return False

        rp=getpass.getpass('Re-Enter New PIN : ')
        if(not rp.isdigit()):
            print("PIN should contain numbers only...")
            msg="Transaction Failed"
            timer(2)
            return False
        elif(len(rp)>4 or len(rp)<4):
            print("PIN must be of 4 Length.. Try Again..")
            msg="Transaction Failed"
            timer(2)
            return False

        if(p==rp and C.changepin(hashlib.md5(p.encode()).hexdigest(),D.acc_id)):
            print("PIN Changed Successfully.")
            msg="PIN Changed"
        else:
            print("PIN not changed.")
            msg="Transaction Failed"
    else:
        print("Date of Birth not matched.")
        msg="Transaction Failed"

    # ADD Code to add transaction to database..
    # transaction_done(transaction_id)

    timer(2)
    
def cash_withdrawl():
    clear()
    header()
    global msg
    try:
        bal=C.fetchbalance(D.acc_id)[0]
    except:
        msg='Transaction Failed'
        print("Server Error")
        timer(1)
        return False
    try:
        withdrawlamount=float(input("Enter Amount you want to withdraw : ")) 
    except ValueError:
        msg='Transaction Failed'
        print("Amount should be number.")
        timer(1)
        return
    except:
        msg="Transaction Failed"
        print("Server Error")
        timer(1)
        return
    
    if(withdrawlamount>bal):
        msg="Transaction Failed"
        print("Balance insufficient to withdraw")
    elif(withdrawlamount<0):
        msg="Transaction Failed"
        print("Withdrawl amount cannot be negative.")
    else:
        try:
            C.cashwithdrawl(D.acc_id,withdrawlamount,bal)
            bal=C.fetchbalance(D.acc_id)[0]
            print("Cash Withdrawl was successful : ",bal)
            global amnt
            msg="Cash Withdrawn"
            amnt=withdrawlamount
        except:
            msg="Transaction Failed"
            print("Server Error")
            timer(1)
    timer(2)
    
def mini_statement():
    clear()
    try:
        transactions=C.ministatement(D.acc_id)
    except:
        msg="Transaction Failed."
        print("Server Error")
        timer(1)
        return
    print()

    

    print("\t\t\t","*"*5,"Account Mini Statement","*"*5)
    print("\t\t ","="*50)
    print("Transaction ID".ljust(20,' '),"Account ID".ljust(20,' '),"Transaction Date".ljust(20,' '),"Transaction Time".ljust(20,' '),"Description".ljust(20,' '),"Amount Withdrawn".ljust(20,' '))
    if(len(transactions)>0):
        with open(str(D.acc_id)+".txt", "w") as f:
            header="Transaction ID".ljust(20,' '),"Account ID".ljust(20,' '),"Transaction Date".ljust(20,' '),"Transaction Time".ljust(18,' '),"Description".rjust(20,' '),"Amount Withdrawn".rjust(20,' ')
            header=convertTuple(header)
            f.write(header+'\n')
            for row in transactions:
                st=''
                for transaction_value in row:
                    st=st+str(transaction_value).ljust(25,' ')
                f.write(st+'\n')
        for row in transactions:
            for transaction_value in row:
                print(str(transaction_value).ljust(21,' '),end='')
            print()
    else:
        print("\t\t No Transaction to Show..")
    try:
        balance=C.fetchbalance(D.acc_id)[0]
        print("current Balance: ",balance)
    except:
        print("Server Error")
    timer(4)

if __name__=="__main__":
    while True:
        amnt=0.00
        msg=""
        D=None
        #Creating Connection object to the database
        C=Connector('my_database.db') 
        #Authenticating the User
        success=authenticate() 
        #Generating Transaction ID
        transaction_id = generate_transaction_id() 
        m=None
        timer(2)
        if success:
            try:
                m=menu() # Getting user choice from menu
            except:
                print("Please Provide valid input")
                m=-1
            if m==1:
                msg="Exiting"
                timer(2)
            elif m==2:
                balance()
            elif m==3:
                pin_change()
            elif m==4:
                cash_withdrawl()
            else:
                msg="Failed Transaction"
                print("Choice should be between 1 to 4.")
                print("You entered wrong choice")
                timer(3)
            clear()
            print("\t\t\t\t\t\t THANK YOU FOR VISITING US! \n You will be redirected to Login Menu in 5 sec.")
            timer(5)
        else:
            m=-1
            clear()
            timer(1)
        try:  
            transaction_done(transaction_id,m,amnt)
        except:
            print("Transaction not completed.")
            timer(2)
        del D
        del C