from datetime import datetime
import re

def header():
   print(dt())
   print(tym())
   print("\t\t\t","*"*20,"WELCOME TO Lakshmi Chit Fund ATM","*"*20,"\n\n") 

def dt():
   return datetime.now().strftime('%Y-%m-%d')

def tym():
   return datetime.now().strftime('%H:%M:%S')

def validate(dob):
   pattern = r'^\d{4}-\d{2}-\d{2}$'
   if re.match(pattern, dob):
      return True
   else:
      return False