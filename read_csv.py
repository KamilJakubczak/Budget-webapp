# -*- coding: utf-8 -*-

# Module that allows to read data from bank extract csv
import csv
import codecs


class Line():

    def __init__(self,date,description,account,category,amount):
        self.date = date.strip()
        self.description = ' '.join(description.split())
        self.account = account.strip(' ')
        self.category = category.strip(' ')
        self.amount = float(''.join(amount.replace('PLN','').replace(',','.').strip().split()))
        if self.amount < 0:
            self.amount = self.amount * -1
    def __str__(self):
        return self.date + '|' + self.description + '|' + self.account + '|' + self.category + '|' + str(self.amount) 

class TransactionList():
    def __init__(self,path):
        self.path = path
        self.filename = self.get_file_name() 
        self.transactions=[]
        self.skipped_lines=[]
        self.read_file()
        self.count_balance()
        

    def read_file(self):

        with codecs.open(self.path,'r', encoding='windows-1250',
                        errors='ignore') as csvfile:
            linereader = csv.reader(csvfile,delimiter=';')
            for row in linereader:
                try:
                    transaction = Line(row[0],(row[1]),
                        (row[2]),(row[3]),(row[4]))
                    self.transactions.append(transaction)
                except Exception as e:
                    self.skipped_lines.append(e)
                    pass

    def count_balance(self):

        balance = 0
        for transaction in self.transactions:
            balance += transaction.amount
            self.balance = balance

    def get_file_name(self):

        end = len(self.path)
        beg = self.path.rfind('/',0,end)+1
        return self.path[beg:end]




