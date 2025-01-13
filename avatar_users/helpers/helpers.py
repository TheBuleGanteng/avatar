import base64
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.contrib.auth import get_user_model
User = get_user_model()
import logging
import os
import re
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from email.mime.text import MIMEText



__all__ = ['check_password_strength', 'EMAIL_ADDRESS_PERSONAL', 'EMAIL_ADDRESS_INFO', 'EMAIL_ADDRESS_DNR', 'filter_usd', 'generate_confirmation_url', 'generate_nonce', 'generate_unique_token', 'AICHAT_PROJECT_NAME', 'pw_req_length', 'pw_req_letter', 'pw_req_num', 'pw_req_symbol', 'readiness_check', 'retrieve_email', 'retrieve_username', 'send_email', 'verify_unique_token']

logger = logging.getLogger('django')



# Validates password strength, subject to the requirements listed below. 
pw_req_length = 4
pw_req_letter = 2
pw_req_num = 2
pw_req_symbol = 0
def check_password_strength(user_input):
    if (
        len(user_input) >= pw_req_length and 
        len(re.findall(r'[a-zA-Z]', user_input)) >= pw_req_letter and 
        len(re.findall(r'[0-9]', user_input)) >= pw_req_num and
        len(re.findall(r'[^a-zA-Z0-9]', user_input)) >= pw_req_symbol
        ):
        return True


# Get email addresses from .env
EMAIL_ADDRESS_PERSONAL= os.getenv('EMAIL_ADDRESS_PERSONAL') 
EMAIL_ADDRESS_INFO = os.getenv('EMAIL_ADDRESS_INFO')
EMAIL_ADDRESS_DNR = os.getenv('EMAIL_ADDRESS_DNR')


# Custom jinja filter: $x.xx or ($x.xx)
def filter_usd(value):
    """Format value as USD."""
    if value >= 0:
        return f"${value:,.2f}"
    else:
        return f"(${-value:,.2f})"


# Generates confirmation url that, when clicked, runs the 
def generate_confirmation_url(route, token, user):
    logger.debug(f'running users app, generate_confirmation_url(user, token) ... function started')
    
    # Encode the user's email with base64 to safely include it in the URL
    encoded_email = urlsafe_base64_encode(force_bytes(user.email))

    # This gives you the relative URL path, assuming your URL pattern expects a 'token' parameter
    relative_url = reverse(f'aichat_users:{route}')
    
    # Append the token and the encoded email as query parameters
    url_with_query_params = f"{relative_url}?token={token}&email={encoded_email}"

    # The value for MY_SITE_DOMAIN (e.g., 'www.example.com' or 'localhost:800') is defined in configs_project and then imported into settings.py
    domain = settings.MY_SITE_DOMAIN
    logger.debug(f'running users app, generate_confirmation_url(token) ... domain is: {domain}')

    # Decide the protocol based on your setup; use 'https' if your site is served over SSL/TLS
    #protocol = 'https'
    #logger.debug(f'running users app, generate_confirmation_url(token) ... protocol is: {protocol}')

    # Construct the full URL
    url = f'{domain}{url_with_query_params}'
    #url = f"{protocol}://{domain}{url_with_query_params}"
    return url


# Generates a nonce to work with Talisman-managed CSP
def generate_nonce():
    logger.debug('running users app, helpers.py ... generate_nonce() ... generated nonce')
    return os.urandom(16).hex()


# Token generation for password reset and registration
def generate_unique_token(user):
    logger.debug(f'running generate_unique_token(user_id)... starting')
    
    # Note that tokens generated via PasswordResetTokenGenerator() are one-time use by default
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    
    logger.debug(f'running generate_unique_token(user)... generated token')
    return token


# Get AICHAT_PROJECT_NAME from .env
AICHAT_PROJECT_NAME = os.getenv("AICHAT_PROJECT_NAME") 


# Readiness check (needed for serving via GCP)
def readiness_check(request):    
    logger.debug(f'starting readiness_check() ... ')

    logger.debug(f'ended readiness_check() ... ')
    return HttpResponse('Ready', status=200)


# Queries the DB to check if user_input matches a registered email. Returns None if no match.
def retrieve_email(user_input):
    logger.info(f'running retrieve_email(user_input) ... function started')
    user = User.objects.filter(email__iexact=user_input).first()
    logger.info(f'running retrieve_email(user_input) ... returned user: { user }')
    return user


# Queries the DB to check if user_input matches a registered email
def retrieve_username(user_input):
    logger.info(f'running retrieve_username(user_input) ... function started')
    user = User.objects.filter(username__iexact=user_input).first()
    logger.info(f'running retrieve_username(user_input) ... returneds user: { user }')
    return user


# Send emails
def send_email(body, recipient, sender, subject):    
    logger.debug(f'running retrieve_username(user_input) ... function started')
    logger.debug(f'running retrieve_username(user_input) ... body is: { body }')
    logger.debug(f'running retrieve_username(user_input) ... recipient is: { recipient }')
    
    try:
        # Path to the service account file
        SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, 'gitignored', 'gmail_access_credentials.json')

        # Define the required scope for sending emails
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']

        # Use the service account to acquire credentials
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # Specify the user to impersonate
        user_to_impersonate = EMAIL_ADDRESS_PERSONAL
        logger.debug(f'running retrieve_username(user_input) ... user_to_impersonate is: { user_to_impersonate }')

        # Impersonate the user
        credentials = credentials.with_subject(user_to_impersonate)

        # Build the Gmail service
        service = build('gmail', 'v1', credentials=credentials)

        # Create a simple MIMEText email
        email_msg = MIMEText(body)
        email_msg['to'] = recipient  # Replace with the recipient's email address
        email_msg['from'] = sender
        email_msg['subject'] = subject

        # Encode the email message in base64
        encoded_message = base64.urlsafe_b64encode(email_msg.as_bytes()).decode()

        # Create the message body
        message_body = {'raw': encoded_message}

        # Send the email
        message = service.users().messages().send(userId='me', body=message_body).execute()
        print(f"Message Id: {message['id']}")

    except Exception as e:
        print(f"An error occurred: {e}")
        raise


# Token validation for password reset and registration
def verify_unique_token(token, user_id):
    logger.debug(f'running verify_unique_token(token, user_id) ... function starting')
    
    try:
        # Initialize the token generator
        token_generator = PasswordResetTokenGenerator()
        
        # Retrieve the user based on the provided user_id
        user = User.objects.get(pk=user_id)

        # Use the token generator to check if the token is valid for the given user
        if token_generator.check_token(user, token):
            logger.debug('Token is valid')
            return user
        else:
            logger.debug('Token is invalid or has expired')
            return None
    except User.DoesNotExist:
        logger.debug('User does not exist')
        return None
    except Exception as e:
        logger.error(f'Error during token verification: {e}')
        return None
