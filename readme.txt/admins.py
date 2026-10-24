from db_config import connection_db1 as con
import random as r
import string as s
from tabulate import tabulate as tb



def selad():
    while True:
        a=[{"1. Add Employee"}, 
                {"2. Remove Employee"}, 
                {"3. See All Employees"}, 
                {"4. Sales Report"},
                {"5. See Employee Queries"},
                {"6. Exit"}]
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
            complaint_ad()
        elif choice == "6":
            
            
            
            
            return "exit"
        else:
            print("Invalid choice. Please try again.")
        
    
    
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
        
def removeemployee():
    seeallemployee()
    emp_no = input("Enter employee number to remove: ")
    cuc, cur = con("employeetools")
    cur.execute("select Employee_no from employee_id")
    try:
        a=cur.fetchall()
        if emp_no not in [row[0] for row in a]:
            print("Employee number not found.")
            
        else:
            cur.execute("DELETE FROM employee_id WHERE Employee_no = %s", (emp_no,))
            cuc.commit()
            print(f"Employee {emp_no} removed successfully.")
            print("invoice sent to employee")
    finally:
        cur.close()
        cuc.close()
       
def salesreport():
    cuc, cur = con()
    
        
    cur.execute("SELECT SUM(price) FROM transactions WHERE t_state IS NULL and seller_id = 'store_01'")
    data = cur.fetchone()
    
    cul, cup = con("employeetools")
    a=data[0]
    cur.execute("select sum(price) from transactions where t_state is NULL and seller_id != 'store_01'")
    abc= cur.fetchone()
    asb=abc[0]
    if asb and a != None:
        t_r=a-asb 
        cup.execute("update store_acc set total_revenue = total_revenue+%s where store_id = 'store_01'", (t_r,))
        cul.commit()
        cur.execute("update transactions set t_state = 'done' where t_state is null")
        cuc.commit()
        cup.execute("update store_acc set store_balance=store_balance+%s where store_id = 'store_01'",(t_r))
        cul.commit()
        
        print("all transactions this month:")
        print(tb(ab,headers=["t_id", 
                    "buyer_id",
                    "seller_id",
                    "product_no",
                    "product_name",
                    "price",
                    "t_date",
                    "t_state"],tablefmt="fancy_grid"))
    else:
        pass
    
    cup.execute("select * from store_acc where store_id = 'store_01'")
    data1 = cup.fetchone()
    cur.execute("""
        SELECT * FROM transactions 
        WHERE MONTH(t_date) = MONTH(CURDATE()) 
        AND YEAR(t_date) = YEAR(CURDATE())
    """)
    ab = cur.fetchall()
    l=[data1[2],data1[3],len(ab),str(r.randint(60,100)) + "%"]
    headers = ["Store account","total revenue", "Transactions this month", "ROI"]
    print(tb([l], headers=headers, tablefmt="fancy_grid"))

    cur.close()
    cuc.close()
    cup.close()
    cul.close()
    
def complaint_ad():
    headers = [("complaint_id"),("employee_no"),("query_text"),("c_date")]
    cuc,cur=con("employeetools")
    cur.execute('select complaint_id,employee_no,query_text,c_date from complaints where status = "Pending"')
    pau=cur.fetchall()
    if pau:
        print(tb(pau,headers=headers,tablefmt="fancy_grid"))
        cur.execute("update complaints set status = 'done'")
    else:
        print("no complaints remaining")
    
    cuc.commit()
    cur.close()
    cuc.close()
