import customer as c
import db_config as db
import tkinter as tk
import employee as emp
import sys

from tabulate import tabulate as tb

print(tb([["WELCOME TO THLH GAMES"]],tablefmt="fancy_grid"))
print("by David,shawn,devan,azba")



db.intialize_db()

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
             ["4)about us"]]
        print(tb(mad,headers=["functions"],tablefmt="fancy_grid"))
        ask=int(input("enter your choice: "))
        if ask == 1:
            emp.emp_login()
            return
        
        elif ask == 2:
            c.select_function()
            
        elif ask == 3:
            print("thank you for visiting us")
            sys.exit()
        elif ask == 4:
            ask1=input("enter password: ")
            if ask1=="anoopnair123":
                b="""In the year of our lord 1678, a high jacker from the Guild of Hodgepodge, named Sir Ben, and a master debater from the Guild of Lolly, named Sir Dover, joined hands.
Together, they branched off their respective guilds and formed in the land of Moidina, the most esteemed Guild of Hodgepodge Lollyhop(GHL).
Sir Ben and Sir Dover used to at first train and supply jesters across the continent of Bangenia, but then, taking inspiration from the CET(Chief Executive Twink) of Twinkistan, 
they decided to foray into the world of entertainment. From parks, theatres, and laundromats to even brothels and photobooths, 
The guild brought all these wondrous innovations to the waiting world.Business was booming until, a difference in opinion came about. Sir Ben wanted to incinerate the indigenous population of 
straight white Malians residing in Moidaniastan, as an act to satisfy the CET. However both the CET and Sir Dover were not into that. Regardless, Sir Ben went through with his plan, and 
thus on the fateful day of the 7th of September, 1701 (now remembered as 7/11) launched his genocidal campaign against the Malians.But Dover, now raised to the rank of Baron, had a contingency. 
He time travelled and transferred his consciousness into Nikki from Obsession,thus preventing all of this with the help of Curry Barker (Somehow), and his expertise in fish frying. 
Together they reset the universe (with the exception of Twinkistan) and decided to diversify into video games. Thus in the year 2026 AC (Alternating Current), Baron Dover
branched of from GHL and brought forth, THE HOUSE OF LOLLYHOP HODGEPODGE."""
                print(b)
            else:
                print("invalid password ")
                entry()
                entry()
                return
                
        else:
            print("not valid choice")
            entry()
            return
    
entry()


    





    

