from django.shortcuts import render

# Create your views here.
from avatar_users.models import Favorites, UserProfile
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import translation
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from .forms import *
from .helpers import *
import logging
import os
import re
logger = logging.getLogger('django')

# Create your views here.
#-------------------------------------------------------------------------


# Get PROJECT_NAME from .env
PROJECT_NAME = settings.PROJECT_NAME 


#-------------------------------------------------------------------------


# Returns the email if registered or otherwise, None
# Used with jsEmailValidation()
@require_http_methods(['POST'])
def check_email_registered(request):
    logger.debug('running users app, check_email_registered_view(request) ... view started')

    email = request.POST.get('user_input', None)
    if email:
        user = retrieve_email(email)
        # If a user object is found, return the email in the JsonResponse
        if user:
            return JsonResponse({'email': user.email})
        else:
            # If no user is found, return a response indicating the email is not taken
            return JsonResponse({'email': None})
    else:
        # If no email was provided in the request, return an error response
        return JsonResponse({'error': 'No email provided'}, status=400)


#-------------------------------------------------------------------------


# Returns '{'result': True}' if user_input meets password requirements and '{'result': False}' if not.
@require_http_methods(["POST"])
def check_password_strength(request):
    logger.debug('running users app, check_password_strength_view(request) ... view started')

    password = request.POST.get('user_input', None)
    if password:
        result = check_password_strength(password)
        return JsonResponse({'result': result})
    else:
        # If no email was provided in the request, return an error response
        return JsonResponse({'error': 'No password provided'}, status=400)


#-------------------------------------------------------------------------


# Checks if password passes custom strength requirements
# Used with jsPasswordValidation()
@require_http_methods(["POST"])
def check_password_valid(request):
    logger.debug('running users app, check_password_valid_view(request) ... view started')

    # Step 1: Pull in data passed in by JavaScript
    password = request.POST.get('password')
    password_confirmation = request.POST.get('password_confirmation')

    # Step 2: Initialize checks_passed array
    checks_passed = []
    logger.debug(f'running users app, check_password_valid_view(request) ... initialized checks_passed array ')    
    
    # Step 3: Start performing checks, adding the name of each check passed to the checks_passed array.
    if len(password) >= pw_req_length:
            checks_passed.append('pw-reg-length')
            logger.debug(f'running users app, check_password_valid_view(request) ... password is: { password } appended pw_reg_length to checks_passed array. Length of array is: { len(checks_passed) }.')
    if len(re.findall(r'[a-zA-Z]', password)) >= pw_req_letter:
            checks_passed.append('pw-req-letter')
            logger.debug(f'running users app, check_password_valid_view(request) ... password is: { password } appended pw_req_letter to checks_passed array. Length of array is: { len(checks_passed) }. ')
    if len(re.findall(r'[0-9]', password)) >= pw_req_num:
            checks_passed.append('pw-req-num')
            logger.debug(f'running users app, check_password_valid_view(request) ... password is: { password } appended pw_req_num to checks_passed array. Length of array is: { len(checks_passed) }. ')
    if len(re.findall(r'[^a-zA-Z0-9]', password)) >= pw_req_symbol:
            checks_passed.append('pw-req-symbol')
            logger.debug(f'running users app, check_password_valid_view(request) ... password is: { password } appended pw_req_symbol to checks_passed array. Length of array is: { len(checks_passed) }. ')
    logger.debug(f'running users app, check_password_valid_view(request) ... checks_passed array contains: { checks_passed }. Length of array is: { len(checks_passed) }.')

    # Step 4: Ensure password and confirmation match
    if password == password_confirmation:    
        confirmation_match = True
    else:
        confirmation_match = False
    logger.debug(f'running users app, check_password_valid_view(request) ... confirmation_match is: { confirmation_match }')

    # Step 5: Pass the checks_passed array and confirmation_match back to JavaScript
    logger.debug(f'running users app, check_password_valid_view(request) ... check finished, passing data back to JavaScript')
    return JsonResponse({'checks_passed': checks_passed, 'confirmation_match': confirmation_match} )


#-------------------------------------------------------------------------


# Returns the username if registered or otherwise, None
# Used with jsUsernameValidation()
@require_http_methods(["POST"])
def check_username_registered(request):
    username = request.POST.get('user_input', None)
    if username:
        user = retrieve_username(username)
        # If a user object is found, return the username in the JsonResponse
        if user:
            return JsonResponse({'username': user.username})
        else:
            # If no user is found, return a response indicating the username is not taken
            return JsonResponse({'username': None})
    else:
        # If no username was provided in the request, return an error response
        return JsonResponse({'error': 'No username provided'}, status=400)


#-------------------------------------------------------------------------


@require_http_methods(["GET", "POST"])
@login_required(login_url='aichat_users:login')
def update_favorites(request):
    logger.debug(f'running aichat_users app, update_favorites() ... function started')

    if request.method == 'POST':
        logger.debug(f'running aichat_users app, update_favorites() ... request via POST')

        expert_id = int(request.POST.get('expert_id'))
        logger.debug(f'running aichat_users app, update_favorites() ... expert_id is: { expert_id }')

        user = request.user
        expert = Expert.objects.get(id=expert_id)
        logger.debug(f'running aichat_users app, update_favorites() ... user is: { user } and expert is: { expert }')
        
        # Check if the favorite relationship already exists
        favorite, created = Favorites.objects.get_or_create(user=user, expert=expert)

        if created:
                    logger.debug(f'running aichat_users app, update_favorites() ... created new favorite relationship between user: { user } and expert: { expert }')
                    return JsonResponse({'success': 'Favorite added'}, status=201)
        else:
            # If the relationship exists, delete it
            favorite.delete()
            logger.debug(f'running aichat_users app, update_favorites() ... deleted existing favorite relationship between user: { user } and expert: { expert }')
            return JsonResponse({'success': 'Favorite removed'}, status=200)

    logger.error(f'running aichat_users app, update_favorites() ... invalid request method: {request.method}')
    return JsonResponse({'error': 'Invalid request method'}, status=405)




#------------------------------------------------------------------------

@require_http_methods(["GET", "POST"])
@login_required(login_url='aichat_users:login')
def favorites_view(request):
    logger.debug(f'running aichat_users app, favorites_view ... view started')

    current_language = request.GET.get('lang', request.session.get('django_language', 'en'))
    logger.debug(f'running aichat_users app, favorites_view ... current_language is: { current_language }')
    
    if current_language:
        translation.activate(current_language)
        logger.debug(f'running aichat_users app, favorites_view ... current_language activated')
        request.session['django_language'] = current_language
        logger.debug(f'running aichat_users app, favorites_view ... request.session[django_language] is: { request.session["django_language"] }')

    user = request.user
    logger.debug(f'running aichat_users app, favorites_view ... current_language is: { current_language }, user is: { user }')

    # Initialize ProfileForm with the user object
    profile_form = ProfileForm(user=user)
    logger.debug(f'running aichat_users app, favorites_view ... pulled ProfileForm')

    # Get the user's favorite experts
    favorites = user.aichat_favorite.all()
    logger.debug(f'running aichat_users app, favorites_view ... favorites retrieved: { favorites }')

    
    favorites_data = []
    
    for favorite in favorites:
        experiences = favorite.expert.experiences.all()
        first_experience = experiences[0] if len(experiences) > 0 else None
        second_experience = experiences[1] if len(experiences) > 1 else None
        total_years = str(int(sum(experience.years for experience in favorite.expert.experiences.all())))

        favorites_data.append({
            'id': favorite.expert.id,
            'name_first': favorite.expert.name_first,
            'name_last': favorite.expert.name_last,
            'photo': favorite.expert.photo,
            'role1': first_experience.role if first_experience else None,
            'employer1': first_experience.employer if first_experience else None,
            'regionCode1': first_experience.geography.region_code if first_experience else None,
            'role2': second_experience.role if second_experience else None,
            'employer2': second_experience.employer if second_experience else None,
            'regionCode2': second_experience.geography.region_code if second_experience else None,
            'total_years': total_years,
            'date_favorited': favorite.added,
            'languages_spoken': ', '.join([language.language.name for language in favorite.expert.languages.all()]),
        })

    # Sort experts by total_score in descending order
    favorites_data.sort(key=lambda x: x['date_favorited'], reverse=True)

    context = {
        'current_language': current_language,
        'favorites_data': favorites_data,
        'profile_form': profile_form,
        'route_used': 'favorites_view',
        'supported_languages': supported_languages_selected,
        'user': user,
        'user_profile': user.aichat_userprofile,
    }
    logger.debug(f'running aichat_users app, index_view ... context passed to the template is: {context}')


    return render(request, 'aichat_users/favorites.html', context)

#-------------------------------------------------------------------------


@require_http_methods(["GET", "POST"])
def login_view(request):
    logger.debug('running login_view ... view started')

    current_language = request.GET.get('lang', request.session.get('django_language', 'en'))
    if current_language:
        translation.activate(current_language)
        request.session['django_language'] = current_language
    logger.debug(f'running login_view ... current_language is: {current_language}')
    
    nonce = generate_nonce()
    logger.debug(f'running login_view ... generated nonce of: {nonce}')
    
    if request.user.is_authenticated:
        logger.debug('running login_view ... user arrived at login already authenticated, logging user out')
        logout(request)
    
    form = LoginForm(request.POST or None)

    context = {
        'current_language': current_language,
        'form': form,  
        'route_used': 'login_view',
    }
    logger.debug(f'running login_view ... context passed to the template is: {context}')

    if request.method == "POST":
        logger.debug('running login_view ... user submitted via POST')

        if form.is_valid():
            logger.debug('running login_view ... user submitted via POST and form passed validation')

            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            logger.debug(f'running login_view ... email is: {email}')

            user = authenticate(request, username=email, password=password)
            logger.debug(f'running login_view ... retrieved user object: {user}')

            if user and user.is_active:
                logger.debug('running login_view ... user found in DB and is active. Logging in.')
                login(request, user)
                messages.success(request, _('Welcome %(first_name)s, you are now logged in to %(PROJECT_NAME)s.') % {
                    'first_name': user.first_name,
                    'PROJECT_NAME': PROJECT_NAME
                })
                logger.debug(f'running login_view ... session data before redirect: {request.session.items()} and session key after login is: {request.session.session_key}')
                
                redirect_url = request.GET.get('next') or reverse('avatar_chat:index')
                redirect_url_with_lang = f'{redirect_url}?lang={current_language}'
                logger.info(f'running login_view ... '
                            f'user is: { user }, '
                            f'redirect_url_with_lang is: {redirect_url_with_lang}, '
                            f'login successful, redirecting to redirect_url_with_lang')
                return redirect(redirect_url_with_lang)

            elif user and not user.is_active:
                logger.debug('running avatar_users app login_view ... '
                             f'user found in DB and is not active. Showing error message.')
                messages.error(request, _('You must confirm your account before logging in. Please check your email inbox and spam folders for an email from %(PROJECT_NAME)s or re-register your account.') % {
                    'PROJECT_NAME': PROJECT_NAME
                })
            else:
                logger.debug('running login_view ... user not found in DB')
                messages.error(request, _('Error: Invalid credentials. Please check your entries for email and password. If you have not yet registered for %(PROJECT_NAME)s, please do so via the link below.') % {
                    'PROJECT_NAME': PROJECT_NAME
                })

        else:
            logger.debug('running login_view ... user submitted via POST and form failed validation')
            messages.error(request, _('Error: Invalid input. Please see the red text below for assistance.'))

    else:
        logger.debug('running login_view ... user arrived via GET')

    return render(request, 'avatar_users/login.html', context)


#-------------------------------------------------------------------------


@require_http_methods(['GET', 'POST'])
@login_required(login_url='avatar_users:login')
def logout_view(request):
    logger.debug('running logout_view ... view started')

    current_language = request.GET.get('lang', request.session.get('django_language', 'en'))
    if current_language:
        translation.activate(current_language)
        request.session['django_language'] = current_language
    user = request.user
    logger.debug(f'running logout_view ... user is: {user}, current_language is: {current_language}')
    
    logout(request)

    form = LoginForm()
    context = {
        'current_language': current_language,
        'form': form,
    }
    logger.debug(f'running login_view ... context passed to the template is: {context}')

    logger.debug('running logout_view ... user is logged out and is being redirected to login.html')
    
    messages.info(request, _('You have been logged out of %(PROJECT_NAME)s.') % {
        'PROJECT_NAME': PROJECT_NAME
    })
    
    return render(request, 'avatar_users/login.html', context)



#-------------------------------------------------------------------------

