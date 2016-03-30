from django.conf.urls import include, url


urlpatterns = [
    url(r'^$', 'facebook_login.views.facebook_login', name="facebook_login"),
    url(r'^authentication/$', 'facebook_login.views.facebook_authentication', name="facebook_authentication"),
    url(r'^email-form/$', 'facebook_login.views.facebook_email_form', name="facebook_email_form"),
    ]
