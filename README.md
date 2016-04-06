# Facebook-auth
Facebook-auth is an easy to setup facebook authentication/registration
mechanism with support for the Django Framework

Quick start
-----------

1. Installation:

    `pip install git+https://github.com/technoarch-softwares/facebook-auth`

2. Add `"facebook_login"` to your `INSTALLED_APPS` setting like this::

    INSTALLED_APPS = (

        ...

        'facebook_login',

    )
    

3.   Add this lines to your project settings file:   
    
     `SITE_URL = 'SITE DOMIAN' #like 'http://localhost:8000/'`
    
     `ERROR_REDIRECT_URL = 'SITE LOGIN URL'`

     `FACEBOOK_REDIRECT_URL = 'facebook/authentication'`

4.  Add Facebook Secret Keys and Client Id    
    
     `FACEBOOK_CLIENT_ID = 'FACEBOOK API KEY'`
    
     `FACEBOOK_CLIENT_SECRET = 'FACEBOOK API SECRET'``
    
5. Include the `facebook_login` URLconf in your project urls.py like this::

    `url(r'^facebook/', include('facebook_login.urls')),`

6. Run `python manage.py migrate` to create the `facebook_login` models.

7. It will create a table into database named by `facebook_login_facebookprofile`.

8. Visit http://127.0.0.1:8000/facebook/ to participate in the facebook authentication.


#Features

1. Access the Facebook API, from Your website (Using OAuth)
        
2. Django User Registration (Convert Facebook user data into a user model)

3. Store user data locally.

4. Facebook FQL access

5. Automated reauthentication (For expired tokens)
