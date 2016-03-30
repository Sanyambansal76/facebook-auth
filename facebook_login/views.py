import requests
import urllib2
import urllib
import json
import ast
import cgi
import json

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_backends, logout
from django.contrib.auth.decorators import login_required

from facebook_login.models import FacebookProfile
from facebook_login.utils import create_username
from facebook_login.forms import EmailForm


facebook_redirect_url = settings.SITE_URL + settings.FACEBOOK_REDIRECT_URL


def facebook_login(request):
    """
    Oauth authentication of the signin user from the facebook.
    Respond back at the redirect_url
    """
    url = "https://graph.facebook.com/oauth/authorize?client_id=%s&redirect_uri=%s" \
        % (settings.FACEBOOK_CLIENT_ID, facebook_redirect_url)

    return HttpResponseRedirect(url)


def get_facebook_access_token(code):
    """
        Code is used to get the access token by use of client id and client secret.
    """
    args = dict(client_id=settings.FACEBOOK_CLIENT_ID, redirect_uri=facebook_redirect_url)
    args["client_secret"] = settings.FACEBOOK_CLIENT_SECRET
    args["code"] = code

    response = cgi.parse_qs(urllib.urlopen(
        "https://graph.facebook.com/oauth/access_token?" +
        urllib.urlencode(args)).read()
    )

    access_token = response["access_token"][-1]

    return access_token


def get_facebook_user_info(access_token):
    """
        Access token is use for getting the linkedin user info and email address.
    """
    graph_url = "https://graph.facebook.com/me?access_token=%s&fields=picture.type(large), email" % access_token
    public_info_url = "https://graph.facebook.com/me?access_token=%s" % access_token

    profile = json.load(urllib.urlopen(graph_url))
    profile_info = json.load(urllib.urlopen(public_info_url))

    profile_response_dict = {}
    profile_response_dict.update(profile)
    profile_response_dict.update(profile_info)
    profile_response_json = json.dumps(profile_response_dict)

    return (profile_response_json, profile_response_dict)


def facebook_authentication(request):
    """
    If facebook provide code then access token will be generated using it
    access token is saved for the user and it is used to fetch the details of the user
    Details of the user can be saved and user can successfully login.
    """
    try:
        code = request.GET['code']
    except:
        messages.error('There is some problem in connecting with facebook at the moment, Please try sign up with email')
        return HttpResponseRedirect('/')

    try:
        access_token = get_facebook_access_token(code)
    except:
        return HttpResponseRedirect(settings.ERROR_REDIRECT_URL)

    try:
        profile_response_json, profile_response_dict = get_facebook_user_info(access_token)
    except:
        return HttpResponseRedirect(settings.ERROR_REDIRECT_URL)

    member_id = str(profile_response_dict['id'])

    try:
        facebook_profile = FacebookProfile.objects.get(facebook_id=member_id)
        user = facebook_profile.user

        if access_token != facebook_profile.access_token:
            facebook_profile.access_token = access_token
            facebook_profile.save()

    except FacebookProfile.DoesNotExist:
        if not 'email' in profile_response_dict:
            request.session['profile_response_dict'] = profile_response_dict
            request.session['profile_response_json'] = profile_response_json
            request.session['member_id'] = member_id
            request.session['access_token'] = access_token

            return HttpResponseRedirect(reverse('facebook_email_form'))
        else:
            try:
                user = User.objects.get(email__iexact=profile_response_dict['email'])
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=create_username(profile_response_dict['name']),
                    email=profile_response_dict['email'],
                    first_name=profile_response_dict['name'],
                )

            FacebookProfile.objects.create(
                user=user,
                facebook_id=member_id,
                access_token=access_token,
                profile_data=profile_response_json,
            )

    user.backend = "django.contrib.auth.backends.ModelBackend"
    login(request, user)

    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


def facebook_email_form(request):
    """
    If email is not provided by the facebook, then an additional email form is there to store the email of the user
    User can enter logged-in successfully
    """
    if not 'profile_response_dict' in request.session:
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        profile_response_dict = request.session['profile_response_dict']
        form = EmailForm(request.POST)

        if form.is_valid():
            try:
                user = User.objects.get(email__iexact=form.cleaned_data['email'])
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=create_username(profile_response_dict['name']),
                    email=form.cleaned_data['email'],
                    first_name=profile_response_dict['name'],
                )

            FacebookProfile.objects.create(
                user=user,
                facebook_id=request.session['member_id'],
                access_token=request.session['access_token'],
                profile_data=request.session['profile_response_json'],
            )

            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)

            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = EmailForm()

    context = {
        'form': form
    }

    return render_to_response('facebook_email_form.html', context, context_instance=RequestContext(request))
