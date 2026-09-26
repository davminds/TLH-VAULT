from db_config import connection_db1 as con
from admins import selad as selad

from tabulate import tabulate as tb


def emp_login():
    cuc, cur = con("employeetools")
    try:
        cur.execute("SELECT employee_no, emp_pwd, employee_name FROM employee_id")
        a = cur.fetchall()
        emp_dict = {row[0]: (row[1], row[2]) for row in a}
        
        cur.execute("SELECT store_id, store_pwd FROM store_acc")
        bs = cur.fetchone()
        
        for _ in range(3):
            ask = input("Enter assigned account id: ")
            
            if bs and ask == bs[0]:
                for _ in range(3):
                    pwd = input("Enter store password: ")
                    if pwd == bs[1]:
                        print("Welcome Admin!")
                        selad()
                        return
                    print("Incorrect password, try again.")
                print("Too many failed password attempts.")
                return

            elif ask in emp_dict:
                emp_pwd, emp_name = emp_dict[ask]
                for _ in range(3):
                    pwd = input("Enter employee password: ")
                    if pwd == emp_pwd:
                        print(f"Welcome {emp_name}!")
                        selemp(ask)
                        return ask
                    print("Incorrect password, try again.")
                print("Too many failed password attempts.")
                from ENTRY import entry
                entry()
                return
                
            else:
                print("Invalid account ID. Please try again.")

        print("Unable to login: Exceeded maximum ID attempts.")
        from ENTRY import entry
        entry()
        return None
    finally:
        cur.close()
        cuc.close()

def seeallgames(emp_no,route_back=True):
    cuc, cur = con()
    try:
        a = ["gameno", "game_name", "platform", "price", "daterel", "genre", "company"]
        cur.execute("select * from games order by gameno")
        bum = cur.fetchall()
        print(tb(bum, headers=a, tablefmt="fancy_grid"))
    finally:
        cur.close()
        cuc.close()
        if route_back:
            selemp(emp_no)

def addgames(emp_no):
    cuc, cur = con()
    try:
        n = int(input("enter no of games to enter: "))
        cur.execute("select game_name from games")
        a=cur.fetchall()
        gms = [row[0] for row in a]
        
        for _ in range(n):
            game = input("enter game name: ")
            if game in gms:
                print("game is already added")
            else:
                plt = input("enter platform: ")
                price = int(input("enter price: "))
                reldate = input("enter release date (YYYY-MM-DD): ")
                genre = input("enter genre: ")
                com = input("enter company: ")
                cur.execute('''insert into games (game_name, platform, price, daterel, genre, company) 
                               values (%s, %s, %s, %s, %s, %s)''', (game, plt, price, reldate, genre, com))
                cuc.commit()
                gms.append(game) # update local list
    finally:
        cur.close()
        cuc.close()
    selemp(emp_no)

def modifygames(emp_no):
    cuc, cur = con()
    try:
        # Pass False so seeallgames() doesn't prematurely trigger selemp()
        seeallgames(emp_no,route_back=False)
        count = int(input("how many games you want to modify: "))
        cur.execute("select gameno from games")
        a = cur.fetchall()
        valid_gamenos = [row[0] for row in a]
        
        if count <= len(valid_gamenos):
            for _ in range(count):
                gno = input("enter game no to modify: ")
                n_changes = int(input('enter no of changes to be made: '))
                for _ in range(n_changes):
                    field = input("what do you want to modify (price/game_name/platform/etc): ")
                    val = input(f"enter new {field}: ")
                    if field == "price":
                        val = int(val)
                    q = f"update games set `{field}` = %s where gameno = %s"
                    cur.execute(q, (val, gno))
                    cuc.commit()
        else:
            print("that's not possible")
    finally:
        cur.close()
        cuc.close()
    selemp(emp_no)

def removegames(emp_no):
    cuc, cur = con()
    try:
        seeallgames(emp_no, route_back=False)
        ask = int(input("how many games to be removed: "))
        l = []
        for _ in range(ask):
            a = int(input("enter game no: "))
            l.append((a,))
        cur.executemany("delete from games where gameno = %s", l)
        cuc.commit()
    finally:
        cur.close()
        cuc.close()
    selemp(emp_no)


def viewid(a):
    h = ["Employee_no", "employee_name", 'emp_pwd', "Employee_job", "Employee_salary", "Hiring_date"]
    cuc, cur = con("employeetools")
    try:
        
        # Fixed typo: empployee_no -> employee_no
        cur.execute("select * from employee_id where employee_no = %s", (a,)) 
        ab = cur.fetchall()
        print(tb(ab, headers=h, tablefmt="fancy_grid"))
    finally:
        cur.close()
        cuc.close()
    selemp(a)

def reportcomplaint(emp_no):
    cuc, cur = con("employeetools")
    try:
        ask = input("do you want to raise a query/complaint to admin? (yes/no): ")
        if ask.lower() == "yes":
            k = input("enter query: ")
            cur.execute("insert into complaints (employee_no, query_text, c_date) values (%s, %s, CURDATE())", (emp_no, k))
            cuc.commit()
            print("your query has been raised to admin")
    finally:
        cur.close()
        cuc.close()
    selemp(emp_no)
def editemployee(emp_no):
    cuc, cur = con("employeetools")
    try:
        
        
        print("\n--- Edit Profile ---")
        print("1. Change Name")
        print("2. Change Password")
        print("3. Change Both")
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == "1":
            new_name = input("Enter new employee name: ")
            cur.execute("UPDATE employee_id SET employee_name = %s WHERE employee_no = %s", (new_name, emp_no))
            cuc.commit()
            print("Name updated successfully!")
        elif choice == "2":
            new_pwd = input("Enter new password: ")
            cur.execute("UPDATE employee_id SET emp_pwd = %s WHERE employee_no = %s", (new_pwd, emp_no))
            cuc.commit()
            print("Password updated successfully!")
        elif choice == "3":
            new_name = input("Enter new employee name: ")
            new_pwd = input("Enter new password: ")
            cur.execute("UPDATE employee_id SET employee_name = %s, emp_pwd = %s WHERE employee_no = %s", (new_name, new_pwd, emp_no))
            cuc.commit()
            print("Profile updated successfully!")
        else:
            print("Invalid choice.")
    finally:
        cur.close()
        cuc.close()
        selemp(emp_no)

def selemp(emp_no):
    while True:
        l = [
            "1) View Profile", 
            "2) See All Games", 
            "3) Add Games", 
            "4) Modify Games", 
            "5) Remove Games",
            "6) Edit Profile", 
            "7) Report Complaint",
            "8) Exit"
        ]
        print(tb([ [item] for item in l ], headers=["Employee Menu"], tablefmt="fancy_grid"))
        choice = input("Enter your choice (1-8): ")
        
        if choice == "1":
            viewid(emp_no)
        elif choice == "2":
            seeallgames(emp_no, route_back=False)
        elif choice == "3":
            addgames(emp_no)
        elif choice == "4":
            modifygames(emp_no)
        elif choice == "5":
            removegames(emp_no)
        elif choice == "6":
            editemployee(emp_no)
        elif choice == "7":
            reportcomplaint(emp_no)
        elif choice == "8":
            from ENTRY import entry
            print("Logging out...")
            entry()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")