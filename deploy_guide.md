# Complete PythonAnywhere Deployment Guide

## 📋 Project Structure

Create this folder structure on your local machine:

```
expense-tracker/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── data/                   # Data storage (will be created automatically)
│   ├── users.json
│   └── expenses.json
└── templates/             # HTML templates
    ├── base.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── expenses.html
    ├── add_expense.html
    └── edit_expense.html
```

## 📦 Step 1: Create requirements.txt

Create a file named `requirements.txt` with this content:

```
Flask==3.0.0
```

## 🚀 Step 2: Sign Up for PythonAnywhere

1. Go to https://www.pythonanywhere.com
2. Click "Start running Python online in less than a minute!"
3. Sign up for a **free Beginner account**
4. Verify your email address

## 📤 Step 3: Upload Your Files

### Option A: Using the Files Tab (Easiest)

1. Log into PythonAnywhere
2. Click on the **"Files"** tab
3. Navigate to `/home/yourusername/`
4. Create a new directory: `expense-tracker`
5. Upload files:
   - Click "Upload a file" and upload `app.py`
   - Click "Upload a file" and upload `requirements.txt`
6. Create a `templates` directory inside `expense-tracker`
7. Upload all HTML template files to the `templates` directory

### Option B: Using Git (Recommended)

1. Create a GitHub repository with your project files
2. In PythonAnywhere, click on **"Consoles"** tab
3. Start a new **Bash console**
4. Run these commands:

```bash
cd ~
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
```

## 🔧 Step 4: Set Up Virtual Environment

In your PythonAnywhere Bash console:

```bash
# Navigate to your project directory
cd ~/expense-tracker

# Create a virtual environment
python3.10 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🌐 Step 5: Configure Web App

1. Click on the **"Web"** tab
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **Python 3.10**
5. Click **Next**

### Configure WSGI File

1. In the Web tab, find the "Code" section
2. Click on the **WSGI configuration file** link (e.g., `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. **Delete all existing content** and replace with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/expense-tracker'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variable for data directory
os.chdir(project_home)

# Import Flask app
from app import app as application
```

**Important**: Replace `yourusername` with your actual PythonAnywhere username!

4. Click **"Save"**

### Configure Virtual Environment

1. Still in the Web tab, find the "Virtualenv" section
2. Enter the path to your virtual environment:
   ```
   /home/yourusername/expense-tracker/venv
   ```
3. Click the checkmark to save

### Set Static Files (Optional, for future CSS/JS)

In the "Static files" section, you can add:
- URL: `/static/`
- Directory: `/home/yourusername/expense-tracker/static/`

## 🔐 Step 6: Security Configuration

### Update Secret Key

1. Go back to Files tab
2. Edit `app.py`
3. Change the secret key line to something secure:

```python
app.secret_key = 'your-very-secure-random-string-here-change-this'
```

Generate a secure key in the Bash console:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as your secret key.

## ✅ Step 7: Launch Your App

1. Go back to the **Web tab**
2. Click the big green **"Reload"** button
3. Wait for the reload to complete
4. Click on your app URL (e.g., `yourusername.pythonanywhere.com`)

Your app should now be live! 🎉

## 📱 Step 8: Access on iPhone

1. Open Safari on your iPhone
2. Go to: `https://yourusername.pythonanywhere.com`
3. Tap the Share button (⬆️)
4. Scroll down and tap **"Add to Home Screen"**
5. Name it "Expense Tracker"
6. Tap "Add"

Now you have a home screen icon that opens your expense tracker!

## 🔍 Troubleshooting

### Error: "Something went wrong"

1. Check the **Error log** in the Web tab
2. Common issues:
   - Wrong path in WSGI file (check username)
   - Virtual environment not configured correctly
   - Missing dependencies

### Import errors

In Bash console:
```bash
cd ~/expense-tracker
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

Then reload the web app.

### File permission errors

```bash
cd ~/expense-tracker
mkdir -p data
chmod 755 data
```

### Can't see changes after updating code

Always click the **"Reload"** button in the Web tab after making changes!

## 🔄 Updating Your App

Whenever you make changes:

1. Upload new files via Files tab or pull from Git:
   ```bash
   cd ~/expense-tracker
   git pull
   ```

2. If you changed `requirements.txt`:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Always reload** the web app in the Web tab

## 📊 Viewing Data

Your data is stored in JSON files in the `data/` directory:
- `data/users.json` - User accounts
- `data/expenses.json` - All expenses

To view or backup:

```bash
cd ~/expense-tracker/data
cat users.json
cat expenses.json
```

## 🔒 Security Notes

**For Production:**

1. **Hash passwords**: Install `werkzeug` and use password hashing:
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   ```

2. **Use environment variables** for secret key:
   ```python
   app.secret_key = os.environ.get('SECRET_KEY', 'fallback-key')
   ```

3. **Consider using a real database** (SQLite or PostgreSQL) instead of JSON files

4. **Add HTTPS** (PythonAnywhere provides this automatically)

## 🎯 Testing Your App

1. Register a new account
2. Log in
3. Add an expense
4. View dashboard
5. Edit an expense
6. Delete an expense
7. Log out and log back in to verify persistence

## 📈 Upgrading (Optional)

Free account limitations:
- One web app
- Custom domain not available
- Limited CPU time

To upgrade:
1. Go to Account tab
2. Choose a paid plan ($5/month)
3. Benefits: multiple apps, more CPU, custom domains

## 🆘 Getting Help

- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
- PythonAnywhere Help: Click "Send feedback" in the dashboard
- Check error logs in the Web tab

## 🎉 Success!

Your expense tracker is now live and accessible from anywhere!

Share your URL: `https://yourusername.pythonanywhere.com`

Enjoy tracking your expenses! 💰📊