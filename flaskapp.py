# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask, render_template, request, redirect, url_for, flash
import creds
import dbCode
import uuid

app = Flask(__name__)
app.secret_key = creds.secret_key

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/display-items')
def display_items():
    query = "SELECT * FROM Inventory;"

    inventory_data = dbCode.execute_query(query)

    return render_template('display_items.html', Inventory=inventory_data)

@app.route('/sql-join')
def display_items_joined():
    query = "SELECT I.ID, I.description, I.price, C.categoryID, C.name  " \
    "FROM Inventory I " \
    "JOIN Category C ON I.categoryID = C.categoryID;" 
    
    joined_inventory_data = dbCode.execute_query(query)

    return render_template('sql_join.html', Inventory=joined_inventory_data)

@app.route('/view-users')
def view_users():
    TABLE_NAME = "Users"

    users_list = dbCode.scan_all_items(TABLE_NAME)

    return render_template('view_users.html', users=users_list)

@app.route('/create-user-page')
def show_create_user_form():
    return render_template('create_user.html')

# I had ai help me here to create a uuid
@app.route('/submit-new-user', methods=['POST'])
def submit_new_user():
    username = request.form.get('username')
    email = request.form.get('email')

    new_user = {
        'uID': str(uuid.uuid4()),
        'username': username,
        'email': email
    }
    
    dbCode.add_user_to_dynamo("Users", new_user) 
    
    return redirect(url_for('view_users'))

@app.route('/delete-user-page')
def show_delete_user_form():
    return render_template('delete_user.html')

@app.route('/submit-delete-user', methods=['POST'])
def submit_delete_user():
    uid_to_delete = request.form.get('uid')

    dbCode.delete_user_from_dynamo("Users", uid_to_delete) 
    
    return redirect(url_for('view_users'))


@app.route('/edit-user-page')
def show_edit_user_form():
    return render_template('edit_user.html')


@app.route('/submit-edit-user', methods=['POST'])
def submit_edit_user():
    uid_to_edit = request.form.get('uid')
    new_username = request.form.get('username')
    new_email = request.form.get('email')

    dbCode.update_user_in_dynamo("Users", uid_to_edit, new_username, new_email) 

    return redirect(url_for('view_users'))

# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
