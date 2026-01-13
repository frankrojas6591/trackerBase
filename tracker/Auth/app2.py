"""
Routes for login / Auth manager
source: 
1. https://github.com/hackersandslackers/flask-blueprint-tutorial
1. https://hackersandslackers.com/flask-login-user-authentication/#:~:text=Initializing%20Flask%2DLogin,__init__.py
1. https://www.google.com/search?q=flask-blueprint+example+for+login+and+user+registration&sca_esv=e373368215e95de4&rlz=1C5CHFA_enUS1122US1122&sxsrf=ANbL-n6MXJnwOs4Td6SailZaS90M2gE4Qw%3A1768221161609&ei=6elkaZjwJIymmtkPn_D5wA0&ved=0ahUKEwjYiOORgYaSAxUMkyYFHR94HtgQ4dUDCBE&uact=5&oq=flask-blueprint+example+for+login+and+user+registration&gs_lp=Egxnd3Mtd2l6LXNlcnAiN2ZsYXNrLWJsdWVwcmludCBleGFtcGxlIGZvciBsb2dpbiBhbmQgdXNlciByZWdpc3RyYXRpb24yBRAAGO8FMggQABiiBBiJBTIFEAAY7wUyBRAAGO8FMggQABiABBiiBEiLeFCUC1jQSHADeAGQAQCYAZYBoAGbDqoBBDAuMTS4AQPIAQD4AQGYAg-gAswMwgIKEAAYsAMY1gQYR8ICChAhGKABGMMEGAqYAwCIBgGQBgiSBwQzLjEyoAfuN7IHBDAuMTK4B70MwgcFNC45LjLIBxqACAA&sclient=gws-wiz-serp



pip install flask flask-login flask-wtf flask-bcrypt flask-sqlalchemy


User Model: Create a User class that inherits from UserMixin and define methods to interact with your database (e.g., checking if a user exists, saving a new user with a hashed password).

Authentication:
Registration: Hash the user's password using generate_password_hash before saving it to the database.

Login: When a user logs in, retrieve the stored hash and use check_password_hash to verify the provided password.

Session Management: Use login_user() to manage the user's session state and logout_user() to terminate it.

Protect Routes: Use the @login_required decorator on views that only authenticated users should access. 

"""

if False:
    ''' blueprint login manager '''
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager
    from config import Config
    
    db = SQLAlchemy()
    login_manager = LoginManager()
    
    def create_app():
        app = Flask(__name__)
        app.config.from_object(Config)
    
        db.init_app(app)
        login_manager.init_app(app)
        login_manager.login_view = 'auth.login' # Specifies the login route
    
        # Register Blueprints
        from .auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
        
        # Import and register other blueprints (e.g., main_bp)
        # from .main import main_bp
        # app.register_blueprint(main_bp)
    
        return app

#####################################

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# Assumes you have a database set up, e.g., with Flask-SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' # Required for sessions/security
# ... database setup (e.g., app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db')

login_manager = LoginManager(app)
login_manager.login_view = 'login' # Specifies the route name for the login page

# --- User Model (Example) ---
# This class needs to be integrated with your actual database model
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash
    
    # Methods required by Flask-Login (get_id is already handled by UserMixin)
    @staticmethod
    def get(user_id):
        # In a real app, query your database to find the user by ID
        # return db.session.query(User).get(user_id)
        pass

@login_manager.user_loader
def load_user(user_id):
    # This function reloads the user object from the user ID stored in the session
    return User.get(user_id) 

# --- Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Retrieve user from database (example placeholder)
        user = User.get_by_username(username) # You need to implement this
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user) # Log the user in
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username already exists
        if User.get_by_username(username): # You need to implement this
            flash('Username already taken', 'warning')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password) # Hash the password
        # Create new user in the database (example placeholder)
        # new_user = User(username=username, password_hash=hashed_password)
        # db.session.add(new_user)
        # db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/dashboard')
@login_required # Protects this route, redirects to login if not authenticated
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
def logout():
    logout_user() # Logs the user out
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# if __name__ == '__main__':
#     app.run(debug=True)