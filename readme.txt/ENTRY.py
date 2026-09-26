import customer as c
import db_config as db
import tkinter as tk
import employee as emp
import sys

from tabulate import tabulate as tb

print(tb([["WELCOME TO TLH GAMES"]],tablefmt="fancy_grid"))
print("by David,shawn,devan,azba)")


db.intialize_db()
print
cuc,cur=db.connection_db1()
cur.execute("delete from cur_cus")
cuc.commit()
cur.close()
cuc.close()
def entry():
    while True:
        ask=input("enter as employee or customer or exit: ")
        
        if ask == "employee":
            emp.emp_login()
            return
        
        elif ask == "customer":
            c.select_function()
            return
        elif ask ==  "exit":
            print("thank you for visiting us")
            sys.exit()
        else:
            print("not valid choice")
            entry()
            return
    
entry()



    

