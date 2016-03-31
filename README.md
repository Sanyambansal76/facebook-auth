# Facebook-auth
Facebook-auth is an easy to setup facebook authentication/registration
mechanism with support for the Django Framework

Quick start
-----------

1. Installation:

    `pip install git+https://github.com/technoarch-softwares/facebook-auth`

2. `Add "facebook_login"` to your `INSTALLED_APPS` setting like this::

    `INSTALLED_APPS = (`

        `...,`

        `'facebook_login',`

    `)`
    
    `SITE_URL = 'SITE DOMIAN' #like 'http://localhost:8000/'`
    
    `ERROR_REDIRECT_URL = 'SITE LOGIN URL'`
    
    `FACEBOOK_CLIENT_ID = 'FACEBOOK API KEY'`
    
    `FACEBOOK_CLIENT_SECRET = 'FACEBOOK API SECRET'`
    
    `FACEBOOK_REDIRECT_URL = 'facebook/authentication'`

3. Include the `facebook_login` URLconf in your project urls.py like this::

    `url(r'^facebook/', include('facebook_login.urls')),`

4. Run `python manage.py migrate` to create the `facebook_login` models.

5. It will create a table into database named by `facebook_login_facebookprofile`.

6. Visit http://127.0.0.1:8000/facebook/ to participate in the facebook authentication.

