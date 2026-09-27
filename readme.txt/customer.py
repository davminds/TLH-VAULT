from tabulate import tabulate as tb

import random as r
import string as s 
from db_config import connection_db1

header=["gameno","game_name","price"]

def create_account():
    cuc, cur = connection_db1()
    accno = None
    
    try:
        cur.execute("select accid,email from customerid") 
        
        a=cur.fetchall()
        existingid = [row[0] for row in a]
        existingemail = [row[1] for row in a]
        
        while True:
            lol = r.randint(10000000, 99999999)
            letters = ''.join(r.choice(s.ascii_letters) for _ in range(2))
            accno = f"{lol}{letters}"
            if accno not in existingid:
                break
                
        print("your account number is: ", accno)
                
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        while True:
            if email.strip() in existingemail:
                print("account with this email id already exists please enter another email")
                email=input("enter your email: ")
            else:
                print("valid email id")
                break
        
        password = input("Enter your password: ")
        query = "INSERT INTO CUSTOMERID (accid, name, email, pwd, wallet) VALUES (%s, %s, %s, %s, 0);"
        cur.execute(query, (accno, name, email, password))
        
        
        aadi = (accno, name, email, password, 0)
        cur.execute("delete from cur_cus")
        cur.execute("insert into cur_cus (accid, name, email, pwd, wallet) values (%s, %s, %s, %s, %s)", aadi)
        
        
        cuc.commit()
        print("Account created successfully!")
        
    finally:
        
        cur.close()
        cuc.close()

    
    ask = input("would you like to add money to your new account?(y/n): ")
    if ask.lower() == "y":
        addmoney(accno)
        return
    else:
        print("ok lets move on")
        select_function()
        return
        
    
    
def logincustomer():
    cuc,cur= connection_db1()
    cur.execute('select * from cur_cus')
    ba=cur.fetchone()
    if ba:
        print("account alr logged in")
        select_function()
        return
    else:
        acc_en=input("enter email: ")
        acc_en=acc_en.strip()
        cur.execute("select email from customerid")
        
        bu=cur.fetchall()
        l = [i[0] for i in bu]
        if acc_en in l:
            pwd_en=input("enter password: ")
            cur.execute("select pwd from customerid where email = %s",(acc_en,))
            pwd=cur.fetchone()[0]
            pwd=pwd_en.strip()
            if pwd_en != pwd:
                print("incorrect password")
                for i in range(3):
                    pwd_en=input("enter password: ")
                    if pwd_en == pwd:
                        print("correct password")
                    else:
                        print("incorrect password")
                        pwd_en=input("enter password: ")
                return
            query="select * from customerid where email = %s and pwd = %s"
            febin=(acc_en,pwd_en)
            cur.execute(query,febin)
            aadi=cur.fetchone()
            if aadi:
                print("login successful")
                cur.execute("delete from cur_cus")
                cur.execute("insert into cur_cus values(%s,%s,%s,%s,%s)",aadi)
                cuc.commit()
                select_function()
                
                
                return "done",acc_en
            
        else:
            ask1=input("would you like to create a new account(1) or exit(anything else): ")
            if ask1 == "1":
                create_account()
                return
                
                
            else:
                select_function()
                return
    cur.close()
    cuc.close()
def select_function():
    cuc,cur=connection_db1()
    functions = [
        ["1) login"],
        ["2) buygame"],
        ["3) sellgame"],
        ["4) exit"],
        ["5) create account"],
        ["6) search games"]
        
    ]
    cur.execute("select * from cur_cus")
    abba=cur.fetchone()
    if abba:
        functions.append(["7) add money"])
        functions.append(["8)see account"])
        
    while True:
        
        print(tb(functions,headers=["function"],tablefmt="fancy_grid"))
        ask=int(input("what function would you like to use (enter nos): "))
        try:
            try:
                if ask == 1:
                    logincustomer()
                elif ask == 2:
                    buygame()
                elif ask == 3:
                    sellgame()
                elif ask == 4:
                    exit()
                elif ask == 5:
                    create_account()
                elif ask == 6:
                    searchgame()
                elif ask == 7:
                    addmoney()
                elif ask == 8:
                    abtacc()
                else:
                    print("please choose a valid option")
            except ValueError:
                print("please choose a valid option")
                cur.close()
                cuc.close()
                select_function()
                return
        except ValueError:
            print("please choose a valid option")
            cur.close()
            cuc.close()
            select_function()
            return
    

    
def buygame(a=None):
    cuc,cur= connection_db1()
    
    
    
    if a==None:
        cur.execute("select gameno, game_name,price  from games order by gameno")
        ab=cur.fetchall()
        print(tb(ab,headers=header,tablefmt="fancy_grid"))
        ask=input("enter game no: ")
    if a=="ringo":
        ask=input("enter game no: ")
    else:
        ask=a
    cur.execute("select gameno,game_name,price from games where gameno= %s",(ask,))
    mdv=cur.fetchone()
    if mdv: # game found
        if a==None:
            print(tb([mdv],headers=["gameno","game name","price"],tablefmt="fancy_grid"))
        
        
        ask1=input("do you want to confirm purchase?(Y/N): ")
        price=mdv[2]
        if ask1.lower() == "y": 
            cur.execute("select * from cur_cus")
            fa=cur.fetchone()
            if fa: #acc logged in
                accid=fa[0]
                tables = ["customerid", "cur_cus"]
                cur.execute("select wallet from cur_cus where accid= %s",(accid,))
                uma= cur.fetchone()
                if uma[0] >= price:#wallet more than game price
                    w_cur=uma[0]-price
                    for i in tables:
                        feb= f"update {i} set wallet = %s where accid = %s"
                        cheri=(w_cur,accid)
                        cur.execute(feb,cheri)
                    cur.execute('''insert into  transactions(buyer_id,
                                seller_id,
                                product_no,
                                product_name,
                                price,
                                t_date) values(%s,"store_01",%s,%s,%s,curdate())''',(accid,mdv[0],mdv[1],price))
                    cuc.commit()
                    ayaan= cur.lastrowid
                    cur.execute("""select t_id,buyer_id,
                                seller_id,
                                product_no,
                                product_name,
                                price,
                                t_date from transactions where t_id = %s """,(ayaan,))
                    abva=cur.fetchone()
                    print(tb([abva],headers=["t_id","buyer_id","seller_id","product_no","product_name","price","t_date"],tablefmt="fancy_grid"))
                    return
                else:
                    print("insuffient funds please add money")   
                    ask2=input("would you like to add money(Y/N): ")
                    if ask2.lower() == "y":
                        addmoney()
                        return
                    else:
                        print("please choose another function or add money")
                        select_function()
                        return
            else:
                print("please login to continue")
                logincustomer()
                return
        else:
            ask3=input("would you like to see our other games?(Y/N): ")
            if ask3.lower() == "y":
                searchgame()
                return
            else:
                select_function()
                return
    else:
        print("sorry game not found, please search for available games")
        print("available games are")
        searchgame()
        return
def sellgame():
    cuc,cur = connection_db1()
    cur.execute("select * from cur_cus")
    eap=cur.fetchone()
    if not eap:
        print("please login and sell game")
        logincustomer()
        return
    n=int(input("how many games you want to sell: "))
    cur.execute("select game_name,price from games")
    abhs=cur.fetchall()
    d=dict(abhs)
    for i in range(n):
        ask=input("enter game name: ")
        if ask in d:
            while True:
                price=int(input("enter asking price: "))
                if price>d[ask]:
                    print("sorry, thats unreasonable. please enter a valid price")
                else:
                    break
        else:
            while True:
                price=int(input("enter asking price: "))
                if price>4500:
                    print("sorry, thats unreasonable. please enter a valid price")
                else:
                    break

        pricer=price-(20/100*price)
        print(f"resale price for {ask} is {pricer}")
        
        lu=ask+"(resale)"
        le=pricer+100
        query="""insert into games(game_name,price)
                values(%s,%s)"""
        lule=(lu,le)
        cur.execute(query,lule)
        nnr=cur.lastrowid
        
        qy="update customerid set wallet=wallet+%s where accid = %s"
        cur.execute(qy,(pricer,eap[0]))
        cuc.commit()
        cur.execute("update cur_cus set wallet=wallet+%s where accid = %s",(pricer,eap[0]))
        cuc.commit()
        print(f"{pricer} has been added to your account")
        cur.execute('''insert into  transactions(buyer_id,
                            seller_id,
                            product_no,
                            product_name,
                            price,
                            t_date) values("store_01",%s,%s,%s,%s,curdate())''',(eap[0],nnr,lu,pricer))
        cuc.commit()
        nvt=cur.lastrowid
        cur.execute("""select t_id,
                    buyer_id,
                            seller_id,
                            product_no,
                            product_name,
                            price,
                            t_date from transactions where t_id = %s""",(nvt,))
        nfz=cur.fetchone()
        
        print(tb([nfz],headers=["t_id","buyer_id","seller_id","product_no","product_name","price","t_date"],tablefmt="fancy_grid"))
    cur.close()
    cuc.close()
def searchgame():
    cuc,cur=connection_db1()
    try:
        cur.execute("select gameno, game_name,price  from games order by gameno")
        ab=cur.fetchall()
        
        print(tb(ab,headers=header,tablefmt="fancy_grid"))
        ask=input("do you want to see more info on a game?(y/n): ")
        if ask.lower() == "y":
            while True:
                j=input('enter gamenumber: ')
                try:
                    if int(j) not in [row[0] for row in ab]:
                        print("Game number not found.")
                        continue
                except ValueError:
                    print("Invalid game number. Please enter a valid number.")
                    continue
                break
            stat=aboutgame(j)
            print(stat)
            ask1=input("do you wanna buy game?(Y/N): ")
            if ask1.lower() == "y":
                buygame(j)
                return
            else:
                ask2=input("do you want to continue browsing(y/n): ")
                if ask2.lower() == "y":
                    searchgame()
                    return
                else:
                    select_function()
                    return
        else:
            ask3=input("do you want to buy a game?: ")
            if ask3.lower()== "y":
                buygame("ringo")
                return
            else:
                select_function()
                return
    finally:
        cur.close()
        cuc.close()

def aboutgame(a=None):
    cuc,cur =connection_db1()
    if a == None:
        
        bum=None
    else:
        cur.execute("select * from games where gameno=%s",(a,))
        adk=cur.fetchone()
        
        bum=tb([adk],headers=["gameno", 
                "game_name", 
                "platform",
                "price",
                "daterel",
                "genre",
                "company"],tablefmt="fancy_grid")
    
    cur.close()
    cuc.close()
    return bum
    
        
        
    
def addmoney(accno=None):
    cuc,cur=connection_db1()
    if accno==None:
        cur.execute("select * from cur_cus")
        nl=cur.fetchone()
        if nl:
            acc=nl[0]
            addmoney(accno=acc)
            return
        else:
            print("please login to add money")
            cur.close()
            cuc.close()
            cur.close()
            cuc.close()
            logincustomer()
            return
    else:
        money=int(input("enter money to be added: "))
        table=["customerid","cur_cus"]
        for i in table:
            query=f"update {i} set wallet=wallet+%s where accid=%s"
            bum=(money,accno)
            cur.execute(query,bum)
            cuc.commit()
        print(f"{money} added to your account")
        cur.close()
        cuc.close()
        select_function()
        return
    
def exit():
    from ENTRY import entry
    cuc,cur= connection_db1()
    cur.execute("delete from cur_cus")
    cuc.commit()
    cur.close()
    cuc.close()
    entry()
    return
def abtacc():
    cuc,cur=connection_db1()
    cur.execute("select * from cur_cus")
    abba=cur.fetchone()
    if abba:
        print(tb([abba], headers=['accid ','name','email', 'pwd' ,'wallet'], tablefmt="fancy_grid"))
        ker=[["1) add money"],
             ["2)change password"],
             ["3)change email"],
             ["4)exit"]]
        print("choose an option: ")
        print(tb(ker,headers=["options"],tablefmt="fancy_grid"))
        ask=int(input("enter option: "))
        while True:
            if ask == 1:
                addmoney(abba[0])
                return
            elif ask == 2:
                newpwd=input("enter new password: ")
                cur.execute("update customerid set pwd=%s where accid=%s",(newpwd,abba[0]))
                cur.execute("update cur_cus set pwd=%s where accid=%s",(newpwd,abba[0]))
                cuc.commit()
                print("password changed successfully")
                cur.close()
                cuc.close()
                return
            elif ask == 3:
                newemail=input("enter new email: ")
                cur.execute("update customerid set email=%s where accid=%s",(newemail,abba[0]))
                cur.execute("update cur_cus set email=%s where accid=%s",(newemail,abba[0]))
                cuc.commit()
                print("email changed successfully")
                cur.close()
                cuc.close()
                return
            elif ask == 4:
                cur.close()
                cuc.close()
                return
            else:
                print("invalid option")
    else:
        print("please login to see account details")
        logincustomer()
        return


