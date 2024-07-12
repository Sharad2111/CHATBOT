
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import create_engine, text
import urllib.parse
import re

# Database connection settings
db_config = {
    'user': "postgres",
    'password': "Sharad@2001",
    'host': "localhost",
    'port': "5432",
    'database': "chatbot_db"
}

# URL-encode the password
encoded_password = urllib.parse.quote(db_config['password'])

# Create a connection string
conn_str = f"postgresql://{db_config['user']}:{encoded_password}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# Create an engine
engine = create_engine(conn_str)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a secure key

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# User model (replace with your actual user model if using a database)
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# Fetch FAQs function
def fetch_faqs():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT question, answer FROM chatbot_data"))
        faqs = result.fetchall()
        return faqs


# Get response function
def get_response(user_input):
    faqs = fetch_faqs()
    for question, answer in faqs:
        pattern = re.compile(re.escape(question), re.IGNORECASE)
        if pattern.search(user_input):
            return answer
    return "I'm sorry, I don't understand your question."


# Route for index page
@app.route('/')
@login_required
def index():
    return render_template('index.html')


# Route for handling user input and getting bot response
@app.route('/get_response', methods=['POST'])
@login_required
def get_bot_response():
    user_input = request.form['user_input']
    response = get_response(user_input)
    print(f"User Input: {user_input}")  # Debugging output
    print(f"Bot Response: {response}")  # Debugging output
    return response


# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Replace with actual authentication logic
        if username == 'Sharad' and password == '2001':
            user = User(id=1)  # Replace with your actual user id retrieval logic
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')


# Route for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))


# Unauthorized handler
@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to access this page.', 'error')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)









# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from sqlalchemy import create_engine, text
# import urllib.parse
# import re
# from flask_mail import Mail, Message

# # Database connection settings
# db_config = {
#     'user': "postgres",
#     'password': "Sharad@2001",
#     'host': "localhost",
#     'port': "5432",
#     'database': "chatbot_db"
# }

# # URL-encode the password
# encoded_password = urllib.parse.quote(db_config['password'])

# # Create a connection string
# conn_str = f"postgresql://{db_config['user']}:{encoded_password}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# # Create an engine
# engine = create_engine(conn_str)

# # Initialize Flask app
# app = Flask(__name__)
# app.secret_key = '122322'  # Replace with a secure key

# # Initialize Flask-Mail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'pandradhika722@gmail.com'
# app.config['MAIL_PASSWORD'] = '122322'  # Replace with your app-specific password
# app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'
# mail = Mail(app)

# # Initialize Flask-Login
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# # User model (replace with your actual user model if using a database)
# class User(UserMixin):
#     def __init__(self, id):
#         self.id = id

#     def get_id(self):
#         return str(self.id)

# @login_manager.user_loader
# def load_user(user_id):
#     return User(user_id)

# # Fetch FAQs function
# def fetch_faqs():
#     with engine.connect() as connection:
#         result = connection.execute(text("SELECT question, answer FROM chatbot_data"))
#         faqs = result.fetchall()
#         return faqs

# # Get response function
# def get_response(user_input):
#     faqs = fetch_faqs()
#     for question, answer in faqs:
#         pattern = re.compile(re.escape(question), re.IGNORECASE)
#         if pattern.search(user_input):
#             return answer
#     return "I'm sorry, I don't understand your question."

# # Route for index page
# @app.route('/')
# @login_required
# def index():
#     return render_template('index.html')

# # Route for handling user input and getting bot response
# @app.route('/get_response', methods=['POST'])
# @login_required
# def get_bot_response():
#     user_input = request.form['user_input']
#     response = get_response(user_input)
#     print(f"User Input: {user_input}")  # Debugging output
#     print(f"Bot Response: {response}")  # Debugging output
#     return response

# # Route for custom query submission
# @app.route('/submit_query', methods=['POST'])
# @login_required
# def submit_query():
#     custom_query = request.form['custom_query']
#     msg = Message("New Custom Query", recipients=['recipient_email@example.com'])
#     msg.body = f"User {current_user.id} submitted a new query:\n\n{custom_query}"
#     mail.send(msg)
#     flash('Your query has been submitted.', 'success')
#     return redirect(url_for('index'))

# # Route for login page
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == ['POST']:
#         username = request.form['username']
#         password = request.form['password']
#         # Replace with actual authentication logic
#         if username == 'Sharad' and password == '2001':
#             user = User(id=1)  # Replace with your actual user id retrieval logic
#             login_user(user)
#             flash('Logged in successfully.', 'success')
#             return redirect(url_for('index'))
#         else:
#             flash('Invalid username or password.', 'error')
#     return render_template('login.html')

# # Route for logout
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('Logged out successfully.', 'success')
#     return redirect(url_for('login'))

# # Unauthorized handler
# @login_manager.unauthorized_handler
# def unauthorized():
#     flash('You must be logged in to access this page.', 'error')
#     return redirect(url_for('login'))

# if __name__ == "__main__":
#     app.run(debug=True)
