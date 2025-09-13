from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)  # One line only

# ---------- Database ----------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------- Admin ----------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('is_admin'):
        return "Access Denied: Admins only!", 403

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image = request.form['image']

        conn = get_db_connection()
        conn.execute('INSERT INTO products (name, price, description, image) VALUES (?, ?, ?, ?)',
                     (name, price, description, image))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('admin.html')

# ---------- Homepage ----------
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('home.html', products=products)

# ---------- Product Detail ----------
@app.route('/product/<int:id>')
def product(id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('product.html', product=product)

# ---------- Cart ----------
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products WHERE id IN (%s)' %
                            ','.join('?'*len(cart_items)), cart_items).fetchall() if cart_items else []
    conn.close()
    return render_template('cart.html', products=products)

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    cart = session.get('cart', [])
    cart.append(id)
    session['cart'] = cart
    return redirect(url_for('index'))  # FIXED from 'home' to 'index'

# ---------- Checkout ----------
@app.route('/checkout', methods=['POST'])
def checkout():
    if 'user_id' not in session:
        return redirect('/login')
    session.pop('cart', None)
    return render_template('checkout_success.html')

# ---------- Login ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password): 
            session['user_id'] = user['id']
            session['is_admin'] = user['is_admin']
            return redirect('/')
        return "Invalid credentials"
    return render_template('login.html')

# ---------- Signup ----------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (name, email, password, is_admin) VALUES (?, ?, ?, ?)',
                         (name, email, password, 0))  # Make is_admin default to 0
            conn.commit()
        except:
            return "Email already exists"
        conn.close()
        return redirect('/login')
    return render_template('signup.html')

# ---------- Logout ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------- Run ----------
if __name__ == '__main__':
    app.run(debug=True)
