# facebook-auth
Authentication using Facebook

Quick start
-----------

1. Add "facebook_login" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'facebook_login',
    )
    
    SITE_URL = 'SITE DOMIAN'
    
    ERROR_REDIRECT_URL = 'SITE LOGIN URL'
    
    FACEBOOK_CLIENT_ID = 'FACEBOOK API KEY'
    
    FACEBOOK_CLIENT_SECRET = 'FACEBOOK API SECRET'
    
    FACEBOOK_REDIRECT_URL = 'facebook/authentication'
    
    #SITE_URL must be terminated with '/' like 'http://localhost:8000/'


2. Include the facebook_login URLconf in your project urls.py like this::

    url(r'^facebook/', include('facebook_login.urls')),

3. Run `python manage.py migrate` to create the facebook_login models.

4. It will create a table into database named by facebook_login_facebookprofile.

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a facebook_login (you'll need the Admin app enabled).

6. Visit http://127.0.0.1:8000/facebook/ to participate in the facebook authentication.

