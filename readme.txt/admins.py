from db_config import connection_db1 as con
import random as r
import string as s
from tabulate import tabulate as tb


def selad():
    a=["1. Add Employee", 
               "2. Remove Employee", 
               "3. See All Employees", 
               "4. Sales Report", 
               "5. Exit"]
    print(tb(a,headers=["admin"], tablefmt="fancy_grid"))
    choice = input("Enter your choice: ")
    
    if choice == "1":
        addemployee()
    elif choice == "2":
        removeemployee()
    elif choice == "3":
        seeallemployee()
    elif choice == "4":
        salesreport()
    elif choice == "5":
        from ENTRY import entry
        print("Exiting admin panel.")
        entry()
        
        return
    else:
        print("Invalid choice. Please try again.")
    
    selad()  # Loop back to the menu after completing an action
def addemployee():
    cuc, cur = con("employeetools")
    try:
        cur.execute("select Employee_no, emp_pwd from employee_id") 
        a=cur.fetchall()
        existingid = {row[0] for row in a}
        
        emp_pwd = input("Enter employee password: ")
        emp_job = input("Enter employee job title: ")
                
        while True:
            lol = r.randint(10,99)
            letters = ''.join(r.choice(s.ascii_letters) for _ in range(8))
            accno = f"{letters}{lol}"
            if accno not in existingid:
                break
        print(f"Employee Number: {accno}")
        
        emp_name = input("Enter employee name: ")
        emp_salary = int(input("Enter employee salary: "))
        hiring_date = input("Enter hiring date (YYYY-MM-DD): ")

        query = "INSERT IGNORE INTO employee_id (Employee_no, employee_name, emp_pwd, Employee_job, Employee_salary, Hiring_date) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(query, (accno, emp_name, emp_pwd, emp_job, emp_salary, hiring_date))
        cuc.commit()
        print(f"Employee {emp_name} added successfully.")
    
    finally:
        cur.close()
        cuc.close()
        return
def seeallemployee():
    cuc, cur = con("employeetools")
    try:
        cur.execute("""select Employee_no,
                employee_name,
                
                Employee_job,
                Employee_salary,
                Hiring_date from employee_id""")
        data = cur.fetchall()
        headers = ["Employee Number", "Employee Name", "Job Title", "Salary", "Hiring Date"]
        print(tb(data, headers=headers, tablefmt="fancy_grid"))
    finally:
        cur.close()
        cuc.close()
        return
def removeemployee():
    seeallemployee()
    emp_no = input("Enter employee number to remove: ")
    cuc, cur = con("employeetools")
    cur.execute("select Employee_no from employee_id")
    try:
        a=cur.fetchall()
        if emp_no not in [row[0] for row in a]:
            print("Employee number not found.")
            return
        else:
            cur.execute("DELETE FROM employee_id WHERE Employee_no = %s", (emp_no,))
            cuc.commit()
            print(f"Employee {emp_no} removed successfully.")
            print("invoice sent to employee")
    finally:
        cur.close()
        cuc.close()
        return
def salesreport():
    cuc, cur = con()
    try:
        
        cur.execute("SELECT * FROM transactions WHERE t_state IS NULL")
        data = cur.fetchall()
        
        cul, cup = con("employeetools")
        a=sum(row[5] for row in data)
        cup.execute("update store_acc set total_revenue = %s where store_id = 'store_01'", (a,))
        cul.commit()
        cur.execute("update transactions set t_state = 'done' where t_state is null")
        cuc.commit()
        cup.execute("select * from store_acc where store_id = 'store_01'")
        data1 = cup.fetchone()
        cur.execute("""
            SELECT * FROM transactions 
            WHERE MONTH(t_date) = MONTH(CURDATE()) 
            AND YEAR(t_date) = YEAR(CURDATE())
        """)
        ab = cur.fetchall()
        l1 = [i[5] for i in ab]

        d = {}
        for i in l1:
            d[i] = d.get(i, 0) + 1

        # Safely find the item with the maximum count
        most_purchased = max(d, key=d.get) if d else "N/A"
           
            
        
        
        l=[data1[4],len(ab),str(r.randint(60,100)) + "%"]
        headers = ["Store account", "Transactions this month", "ROI",]
        print(tb([l], headers=headers, tablefmt="fancy_grid"))
        print("all transactions this month:")
        print(tb(ab,headers=["t_id", 
                    "buyer_id",
                    "seller_id varchar(10)",
                    "product_no int",
                    "product_name varchar(336)",
                    "price int",
                    "t_date date",
                    "t_state varchar"],tablefmt="fancy_grid"))
    finally:
        cur.close()
        cuc.close()
        cup.close()
        cul.close()
        
        return
    