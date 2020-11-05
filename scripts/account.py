import cryptography
from cryptography.fernet import Fernet
import pandas as pd
import os
import random

class account:
    
    def __init__ (self, userName = "", password = ""):
        self._scriptPath = os.path.dirname(os.path.abspath(__file__))
        self._userName = userName
        self._password = password
        self._homePath = self._scriptPath.replace("\\scripts", "")
        self._dataPath = self._scriptPath.replace("\\scripts", "\\data\\")
        self._fields = "Store", "price", "Referrence", "Memo", "date", "card"
        self._categories = "Grocery", "Gas", "Clothes", "Fun", "Alcohol", "Restaurant", "Rent", "Utilities", "Taxes"
        self._finDF = pd.DataFrame()
        self._finFileName = ""

    def checkSetup (self):
        if os.path.isdir(self._dataPath):
            return
        else:
            os.mkdir(self._dataPath)
            self.__setupLogin__()
            self.__setupUserData__("admin")

    def __del__ (self):
        print("user del")

    def setUser (self, userName, password):
        self._userName = userName
        self._password = password
    
    # Verifies whether username and password combo is in logins table
    # returns bool whether verified or not
    def verifyUser (self):
        credentials, fileName = self.__getDF__("Logins")
        try:
            word = credentials.loc[credentials['username'] == self._userName, 'password'].iloc[0]
        except:
            return False
        if (word == self._password):
            self.__setFinDF__()
            return True
        else:
            return False


    # adds user and password to logins table
    def addUser (self, user, password):
        credentials, oldFile = self.__getDF__("Logins")
        print(credentials)
        print("----------------------")
        credentials = credentials.append({"id": 1001, "username": user, "password":password} ,ignore_index = True)
        print(credentials)
        self.__writeFile__("Logins", oldFile, credentials)
        self.__setupUserData__(user)

    def addReceipt (self, entry):
        ID = self.__getUniqueID__()
        while (ID in self._finDF['id']):
            ID = self.__getUniqueID__()
        self._finDF = self._finDF.append({"id":ID, "store":entry[0], "price":entry[1], "reference":entry[2],
                            "category":entry[6],"card":entry[5], "date":entry[4], "memo":entry[3]},
                            ignore_index = True)

    def __setFinDF__ (self) :
        self._finDF, self._finFileName = self.__getDF__(self._userName + "DATA")

    def getFinDF (self):
        return self._finDF

    #returns username
    def getUser (self):
        return self._userName

    def getFields (self):
        return self._fields

    def getCategories (self):
        return self._categories


    def __getUniqueID__ (self):
        return random.randrange(99999)

    # returns pandas df and filename
    def __getDF__ (self, fileName):
        encryptedName = ""
        found = False
        pandasDF = pd.DataFrame
        for entry in os.listdir(self._dataPath):
            if entry.endswith(".encrypted"):
                name = os.path.splitext(entry)[0]
                name = name.replace(self._dataPath, "")
                if (self.__decrypt__(bytes(name, 'Ascii')) == fileName): #Check for encrypted file that matches fileName
                    encryptedName = self._dataPath + entry
                    with open(encryptedName, 'rb') as f:
                        data = f.read()
                        DF = self.__decrypt__(data)
                        pandasDF = pd.read_json(DF)
                        found = True
        if not found:
            print ("FILE NOT FOUND")
        #print("DATAFRAME - " + pandasDF)
        return pandasDF, encryptedName

    def __decrypt__ (self, data):
        F = Fernet(self.__getFernetKey__())
        decrypted = F.decrypt(data)
        return decrypted.decode('utf-8')

    # Returns the fernet key specidfic to users .ssh key
    def __getFernetKey__ (self):
        with open(".ssh/id_rsa.pub") as f:
            data = f.read()
            data = data[8:51] + "="
            data = bytes(data, 'Ascii')
        #print(data)
        return data

    # Param data        String in which to encrypt
    # Returns encrypted data in bytes.
    def __encrypt__ (self, data):
        data = bytes(data, 'Ascii')
        F = Fernet(self.__getFernetKey__())
        return F.encrypt(data)

    def __writeFile__ (self, fileName, oldFile, payload) :
        print("file name: " +  fileName)
        encryptedName = (self.__encrypt__(fileName)).decode('utf-8')
        payload = payload.to_json()
        payload = self.__encrypt__(payload)
        with open(self._dataPath + encryptedName + ".encrypted", 'wb') as f:
            f.write(payload)
        try:
            os.remove(oldFile)
            print("Deleted - " +oldFile)
        except:
            print("NO FILE FOUND TO DELETE")
        return

    def save (self):
        if (self._userName != ""):
            self.__writeFile__(self._userName + "DATA" , self._finFileName , self._finDF)
            print("save")

    def ToString (self):
        print(self._userName)
        print(self._password)

    def __setupUserData__(self, name):
        print("data")
        financeDF = pd.DataFrame(columns = ["id", "store", "price", "reference", "category", "card", "date", "memo"])
        jsonFinDF = financeDF.to_json()
        encryptedFinDF = self.__encrypt__(jsonFinDF)
        encryptName = self.__encrypt__(name + "DATA").decode('utf-8')
        with open(self._dataPath + encryptName + ".encrypted", 'wb') as f:
            f.write(encryptedFinDF)

    def __setupLogin__ (self):
        print("logins")
        df = pd.DataFrame(columns=["id", "username", "password"])
        df = df. append({"id":1001, "username": "admin", "password": "password"}, ignore_index=True)
        jsonDF = df.to_json()
        encryptedDF = self.__encrypt__(jsonDF)
        encryptName = self.__encrypt__("Logins").decode('utf-8')
        with open(self._dataPath + encryptName + ".encrypted", 'wb') as f:
            f.write(encryptedDF)

    #def setup (self):
       # financeDF = pd.DataFrame(columns = ["id", "store", "price", "reference", "category", "card", "date", "memo"])
        #jsonFinDF = financeDF.to_json()
       # encryptedFinDF = self.__encrypt__(jsonFinDF)
        #print(encryptedFinDF)
        #encryptName = self.__encrypt__(self._userName + "DATA").decode('utf-8')
       # with open(self._dataPath + encryptName + ".encrypted", 'wb') as f:
       #     f.write(encryptedFinDF)
        #df = pd.DataFrame(columns=["id", "username", "password"])
        #df = df.append({"id": 1001, "username": "admin", "password":"password"} ,ignore_index = True)
        #print(df)
        #jsonDF = df.to_json()
        #print(jsonDF)
        #jsonDF = jsonDF.encode('utf-8')
        #fernet = Fernet(self.__getFernetKey__())
        #encrypted = fernet.encrypt(jsonDF)
        #print(encrypted)
        #encryptName = (self.__encrypt__("Logins")).decode('utf-8')
        #print(self.dataPath + encryptName + ".encrypted")
        #with open((self._dataPath + encryptName + ".encrypted"), 'wb') as f:
        #   f.write(encrypted)
        #return
       # print(encrypted)
       # with open("../data/")

          


