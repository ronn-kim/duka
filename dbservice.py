import psycopg2

# connecting to the server
conn = psycopg2.connect(
    dbname = 'duka',
    user='postgres',
    host='localhost',
    password= 'sage@#4839',
    port= 5432
) 
# cursor connection
cur = conn.cursor()

# fetching data
def get_data(table_name):
    query = f"SELECT * FROM {table_name};"
    cur.execute(query)
    data =cur.fetchall()
    return data
# inserting data 
def insert_data(values):
    query = "INSERT INTO products(product_name, buying_price, selling_price, stock_quantity) values(%s,%s,%s,%s);"
    cur.execute(query, values)
    conn.commit()

# making a sale
def insert_sale(values):
    query ="INSERT INTO sales (product_id, quantity, created_at) VALUES (%s, %s, now());"
    cur.execute(query,values)
    conn.commit()


# inserting users
def insert_user(values):
    query = 'INSERT INTO users(user_name,email,password) values(%s,%s,%s);'
    cur.execute(query, values)
    conn.commit()

# cheking email
def check_email(email):
    query = "SELECT * FROM users WHERE email = %s"
    cur.execute(query,(email,))
    data = cur.fetchall()
    return data

# cheking email and password
def check_email_password(email,password):
    query='SELECT * FROM users WHERE email=%s and password=%s'
    cur.execute(query,(email,password))
    data = cur.fetchall()
    return data

# sales product
def sales_product():
    query="SELECT p.product_name, SUM(p.selling_price * s.quantity)\
         AS totalsales FROM sales as s JOIN products as p ON s.product_id = p.product_id\
            GROUP BY p.product_name;"
    cur.execute(query)
    data = cur.fetchall()
    return data

# profit
def profit_d():
    query = "SELECT p.product_name , SUM((p.selling_price - p.buying_price)\
        * s.quantity) AS profit FROM sales as s JOIN products as p ON s.product_id = \
            p.product_id GROUP BY p.product_name;"
    cur.execute(query)
    data = cur.fetchall()
    return data

# daily sales
def sales_daily():
    query ="SELECT DATE(s.created_at) AS sales_day, SUM(p.selling_price * s.quantity)\
        AS sales FROM sales s JOIN products p ON s.product_id = p.product_id GROUP\
            BY sales_day ORDER BY sales_day;"
    cur.execute(query)
    data = cur.fetchall()
    return data

# daily profit
def daily_profit():
    query = "SELECT DATE(sales.created_at) as profit_day,\
        SUM((products.selling_price - products.buying_price)* sales.quantity)\
            AS profit from sales JOIN products on sales.product_id = products.product_id\
                GROUP BY profit_day ORDER BY profit_day;"
    cur.execute(query)
    data = cur.fetchall()
    return data

# sum of the users sales
def user_total():
    query='SELECT u.users_id, SUM(s.quantity) AS total_sales\
        FROM users u JOIN sales s ON u.users_id = s.users_id\
            GROUP BY u.users_id;'
    cur.execute(query)
    data=cur.fetchall()
    return data






  




