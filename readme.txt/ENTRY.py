import customer as c
import db_config as db

import employee as emp
import sys
import maskpass as mp

from tabulate import tabulate as tb

print(tb([["WELCOME TO THLH GAMES"]],tablefmt="fancy_grid"))
print("by David,shawn,devan,azba")
a=mp.askpass(prompt="enter mysql password: ",mask="*")

try:
    db.intialize_db(a)
except:
    print("Could not connect to database. please try again")
    sys.exit()

cuc,cur=db.connection_db1()
cur.execute("delete from cur_cus")
cuc.commit()
cur.close()
cuc.close()
def entry():
    while True:
        mad=[["1) employee"],
             ["2) customer"],
             ["3) exit"],
             ]
        print(tb(mad,headers=["functions"],tablefmt="fancy_grid"))
        ask=int(input("enter your choice: "))
        if ask == 1:
            emp.emp_login()
            
        
        elif ask == 2:
            
            c.select_function()
            
            
        elif ask == 3:
            print("thank you for visiting us")
            sys.exit()
        
                
        else:
            print("not valid choice")
            entry()
            return
    
entry()

    





    

