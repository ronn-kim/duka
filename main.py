from flask import Flask,render_template,redirect,request,url_for,flash,session
from dbservice import get_data,insert_data,insert_user,check_email,check_email_password,sales_product,sales_daily,profit_d,daily_profit,insert_sale
# from encrypt import hashing_password
from flask_bcrypt import Bcrypt 


app = Flask(__name__)
bcrypt=Bcrypt(app)
app.secret_key = "a6c25807b7427eaac17924d648aeab"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        # sales per day
        sale_P = sales_product()
        p_name=[]
        p_sale=[]
        for i in sale_P:
            p_name.append(str(i[0]))
            p_sale.append(i[1])

        print(p_name)
        print(p_sale)
        # profit per product
       
        p_day=profit_d()
        rr=[]

        for i in p_day:
            rr.append(float(i[1]))

        print(rr)

        # sales per day
        s_d = sales_daily()
        # date=[]
        # sale_d=[]

        # for i in s_d:
        #     date.append(str(i[0]))
        #     sale_d.append([i[1]])

        # print(date)
        # print(sale_d)
        # daily profit
        
        profit_data = daily_profit()
        profit_dates = []
        profit_values = []

        for profit in profit_data:
            profit_dates.append(str(profit[0]))
            profit_values.append(profit[1])
        print(profit_dates)
        print(profit_values)
    else:
        flash("Access Denied: Admins Only",403)
        return redirect(url_for('login'))

    return render_template('dashboard.html', p_name=p_name,p_day=p_day,p_sale=p_sale,s_d=s_d,rr=rr,profit_data=profit_data,profit_dates=profit_dates,profit_values=profit_values)

@app.route('/products')
def products():
    prod = get_data('products')
    return render_template('products.html', product=prod)

@app.route('/add_products',methods=['POST', 'GET'])
def add_products():
    if request.method == "POST":
        pname = request.form['product_name']
        bprice = request.form['buying_price']
        sprice = request.form['selling_price']
        squantity = request.form['stock_quantity']
        # insert into db
        new_prod = (pname, bprice, sprice, squantity)
        insert_data(new_prod)
        flash('product added successfuly')


    return redirect(url_for('products'))

@app.route('/sales')
def sales():
    sale = get_data('sales')
    prod=get_data('products')
    return render_template('sales.html', sales=sale,products=prod)

@app.route('/make_sale',methods=['GET', 'POST'])
def make_sale():
    if request.method == 'POST':
        product_name = request.form['product_name']
        quantity = request.form['quantity']
        new_sale=(product_name, quantity)
        insert_sale(new_sale)
        flash('Sale made')

    return redirect(url_for('sales'))

@app.route('/register', methods=["POST", "GET"])
def register():
    
    if request.method == "POST":
        uname = request.form['full_name']
        mail=  request.form['email']
        passw= request.form['password']

        # hashing
        hashed=bcrypt.generate_password_hash (passw).decode('utf-8')
        
       
        # insert into db
        new_user =(uname,mail,hashed)
        c_email=check_email(mail)
        print (c_email)
        if len(c_email) == 0:
            insert_user(new_user)
            flash ("registered successfuly")
            return redirect(url_for('log_in'))
        else:
            flash ('Email already exists')

    return render_template('register.html')

@app.route('/log_in',methods=['POST', "GET"])
def log_in():
   
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
     
        c_mail= check_email(email)
        print (c_mail)
        if len(c_mail) == 1:
            session['email']=email
            check_em_ps = check_email_password(email,password)
            if len(check_em_ps) == 1:
                flash('You were successfully logged in')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials')
        else:
            flash ('Email does not exists')
            redirect(url_for('register'))

    return render_template('login.html')
@app.route('/forgot_password')
def forgot_password():

    return render_template('forgot_password.html')

@app.route('/inventories')
def inventories():
    return render_template('inventorie.html')

@app.route('/users')
def users():

    return render_template('users.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/manage')
def manage():
    return render_template('/manage.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))


if __name__ == ('__main__'):
    app.run(debug=True)


