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


from flask import Blueprint, render_template

# Blueprint Configuration
bp = Blueprint("bpAuth", __name__, template_folder="templates", static_folder="static")


@bp.route("/<ext>/profile/", methods=["GET"])
def user_profile(ext) -> str:
    """
    Logged-in user profile page.

    :ext is profile within extension

    :returns: str
    """
    user = fake.simple_profile()
    job = fake.job()
    return render_template(
        "profile.jinja2",
        title="User Profile",
        template="profile-template",
        user=user,
        job=job,
    )

