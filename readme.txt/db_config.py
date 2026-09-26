import mysql.connector as mysql
a=""
def intialize_db():
    global a
    a=input("Enter your mysql password: ")
    cuc=mysql.connect(host="localhost",user="root",password=a)
    cur=cuc.cursor()
        
    cur.execute("create database if not exists customertools")
    cur.execute("use customertools")
    cur.execute("""create table if not exists customerid(accid varchar(10) primary key,
                name varchar(20)
                ,email varchar(100)
                ,pwd varchar(20),
                wallet int
                )""")
    cur.execute("""create table if not exists games(gameno int auto_increment primary key, 
                game_name varchar(336) unique, 
                platform varchar(25),
                price int,
                daterel date,
                genre varchar(25),
                company varchar(50))auto_increment=100""")
    games_data=[("Minecraft","PC",2250,"2009-05-17","sandbox","Mojang"),
                ("Red Dead Redemption 2","PS4/PS5",4599,"2018-10-26","action-adventure","Rockstar"),
                ("Tomb raider","PC",2390,"2013-03-05","action-adventure","Crystal dynamics"),
                ("Horizon zero dawn","PS4/PS5",1499,"2017-02-28","action-rpg","Guerrilla Games"),
                ("Uncharted 4: A Thieves End","PS4/PS5",1199,"2016-05-10","action-adventure","Naughty dogs")
                ]
    query='''insert ignore into games(game_name,platform,price,daterel,genre,company)
           values (%s,%s,%s,%s,%s,%s)'''
    
    cur.executemany(query,games_data)
    cur.execute('''create table if not exists transactions(t_id int auto_increment primary key, 
                    buyer_id varchar(10),
                    seller_id varchar(10),
                    product_no int,
                    product_name varchar(336),
                    price int,
                    t_date date,
                    t_state varchar(4) default null) auto_increment=100''')
    cur.execute("""create table if not exists cur_cus(accid varchar(10) primary key,
                name varchar(20)
                ,email varchar(100)
                ,pwd varchar(20),
                wallet int)""")
    cuc.commit()
    cur.execute("""create database if not exists employeetools""")
    cur.execute("use employeetools")
    cuc.commit()
    cur.execute("""create table if not exists store_acc
                (store_id varchar(10) primary key,
                store_pwd varchar(10), 
                store_balance int,
                store_revenue int,
                
                total_revenue int)""")
    cur.execute(" insert ignore into store_acc values('store_01','Minds@2009',100000,0,0)")
    cur.execute("""create table if not exists employee_id
                (Employee_no varchar(10) primary key,
                employee_name varchar(100),
                emp_pwd varchar(20),
                Employee_job varchar(50),
                Employee_salary int,
                Hiring_date date)""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        complaint_id INT AUTO_INCREMENT PRIMARY KEY,
        employee_no VARCHAR(10),
        query_text TEXT,
        c_date DATE,
        status VARCHAR(20) DEFAULT 'Pending'
    )
""")
    cur.execute("insert ignore into employee_id values('ABhjMkji09','Maadhav anoop','Crazymaadhav09','Janitor',50000,'2022-01-15')")
    cuc.commit()
    cur.close()
    cuc.close()
    
def connection_db1(b="customertools"):
    
    cuc=mysql.connect(host="localhost",user="root",password=a,database=b)
    cur=cuc.cursor()
    return cuc,cur
    

    

    
