# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash, session
import dbCode
import creds

app = Flask(__name__)
app.secret_key = creds.secret_key

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # Get the data submitted from the form
        username = request.form['username']
        password = request.form['password']
        
        # Hardcoded check for simplicity (you can connect this to a DB later!)
        if username == 'admin' and password == 'password123':
            # Store the user in the session to "remember" they are logged in
            session['logged_in'] = True
            session['username'] = username
            # Redirect them to the main inventory page
            return redirect(url_for('display_inventory'))
        else:
            error = 'Invalid Credentials. Please try again.'
            
    # If it's a GET request, just show the login page
    return render_template('login.html', error=error)


@app.route('/display-items')
def display_users():
    query = "SELECT * FROM Inventory;"

    inventory_data = dbCode.execute_query(query)

    return render_template('display_items.html', Inventory=inventory_data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 1. Get the data from the registration form
        new_username = request.form['username']
        new_password = request.form['password']
        
        # 2. Write the SQL query to insert the new user
        # Note: In a production app, you MUST encrypt/hash passwords before saving them!
        query = "INSERT INTO users (username, password) VALUES (%s, %s);"
        
        # 3. Use your new helper function to save the data securely
        dbCode.execute_insert(query, (new_username, new_password))
        
        # 4. Send them back to the login page so they can log in
        return redirect(url_for('login'))
        
    # If it's a GET request, just show the form
    return render_template('create_account.html')

# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
