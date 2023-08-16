import sqlite3

class Connector:
    cursor=None
    conn=None

    def __init__(self,databasename):
        self.conn = sqlite3.connect(databasename)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def getdata(self,cn):
        statement='Select PIN,Account_ID,Card_Number,DOB from Accounts  WHERE Card_Number = ?'
        data=None
        
        data=self.cursor.execute(statement,(cn,))
        dt=None

        for row in data:
            # print(row)
            dt=row

        return dt
        # print(pin)
        # return pin[0]

    def fetchbalance(self,acc_id):
        statement='Select Balance from Accounts  WHERE Account_ID = ?'

        data=None
        
        data=self.cursor.execute(statement,(acc_id,))
        bal=None

        for row in data:
            # print(row)
            bal=row

        return bal

    def changepin(self,pin,acc_id):
        statement='Update Accounts SET PIN=?  WHERE Account_ID = ?'

        data=None
        
        data=self.cursor.execute(statement,(pin,acc_id))
        # print(data)
        self.conn.commit()
        return True
    
    def cashwithdrawl(self,acc_id,withdrawlamount,bal):
        statement='Update Accounts SET Balance=?  WHERE Account_ID = ?'

        data=None
        
        data=self.cursor.execute(statement,((bal-withdrawlamount),acc_id))
        # print(data)
        self.conn.commit()
        return True

    def addtransaction(self,transaction_id,acc_id,transaction_date,transaction_time,description,amount):
        statement='INSERT INTO Transactions VALUES(?,?,?,?,?,?)'

        data_tuple=(transaction_id,acc_id,transaction_date,transaction_time,description,amount)

        self.cursor.execute(statement,data_tuple)

        self.conn.commit()
        return True
    
    def ministatement(self,acc_id):
        statement='Select * from Transactions  WHERE Account_ID = ? ORDER BY Transaction_Date DESC, Transaction_Time DESC LIMIT 5'
        data=None
        
        data=self.cursor.execute(statement,(acc_id,))
        dt=[]

        for row in data:
            dt.append(row)

        
        return dt
 