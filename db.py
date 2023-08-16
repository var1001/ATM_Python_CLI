import sqlite3
import hashlib

# Creating or Connecting to the existing database.
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Accounts
               (Account_ID VARCHAR(20) PRIMARY KEY,Balance MONEY NOT NULL,DOB DATE NOT NULL,Lastname VARCHAR(35),
               Firstname VARCHAR(35) NOT NULL,Card_Number VARCHAR(20) NOT NULL UNIQUE,
               PIN CHAR(32))
               """)
print('Table created successfully.'),


cursor.execute("""CREATE TABLE IF NOT EXISTS Transactions
               (Transaction_ID VARCHAR(15) PRIMARY KEY,Account_ID VARCHAR(20) NOT NULL,Transaction_Date DATE NOT NULL,
               Transaction_Time TIME NOT NULL ,Description TEXT NOT NULL,Amount MONEY,
               FOREIGN KEY (Account_ID) REFERENCES Accounts(Account_ID))""")

print("Transaction table created successfully.")



statement='INSERT INTO Accounts VALUES(?,?,?,?,?,?,?)'

pin="4321"
hashed=hashlib.md5(pin.encode()).hexdigest()
data_tuple=(1001,10000,"1998-10-10","Jain","Vardhan","154745693654",hashed)
cursor.execute(statement,data_tuple)

print("Printing length of  hashed value: ",len(hashed))

data_tuple=(1002,10000,"1999-11-16","Goyal","Raghav","789634517896",hashed)
cursor.execute(statement,data_tuple)
data_tuple=(1003,10000,"2000-01-21","Arora","Anshul","789654125489",hashed)
cursor.execute(statement,data_tuple)
data_tuple=(1004,10000,"1997-04-07","Sharma","Mohit","456987789541",hashed)
cursor.execute(statement,data_tuple)

cursor.execute('SELECT * FROM Transactions')
# rows=cursor.fetchmany(2)
for row in cursor.fetchall():
    print(row)


cursor.close()
conn.commit()
conn.close()