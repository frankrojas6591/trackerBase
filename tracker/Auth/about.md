# Authentication of `tracker` apps

You must understand that for one application you must use `one login manager` no matter how many blueprints you use 
- there are some exceptions, for example when blueprints are independent, 
- `tracker` is the underlying data manager for a personalized AI agent
    - thus we use a single login-manager via flask-login
 

## Why 1 entry point

- You have 1 entry point
- for any app, if user is not logged in, he will be redirected to login/registration page
- You have 1 user loader


## How login manager works:

1. It registers current_user in request context
1. before_request reads your session,
2. gets user id,
3. loads the user with user_loader and
4. set it to current_user or AnonymousUser

When you visit the private page, login_required checks current_user.is_authenticated() else redirects to login page
On login, it adds user id to the session
So you must initialize only one login manager instance for flask application and then use login_required and current_user in all your blueprints.