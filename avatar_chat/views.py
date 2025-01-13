import logging
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.utils.timezone import now
from .forms import *
from .helpers import stream_response_to_user
import os
import uuid

# Create your views here.


logger = logging.getLogger('django')





@require_http_methods(['GET', 'POST'])
@login_required(login_url='aichat_users:login')
def stream_response(request):

    user = request.user

    # POST: Handles form submission, validates the form, and stores the input along with a generated stream_id in the session.
    if request.method == 'POST':
        
        input_form = InputForm(request.POST) # Display the InputForm

        if input_form.is_valid(): # Check for form validity
            logger.debug(f'running stream_response() ... user submitted via post and form passed validation')

            input_text = input_form.cleaned_data.get('user_input')
            conversation_id = user.aichat_userprofile.conversation_id
            logger.debug(f'running stream_response() ...' 
                         f'input_text is: { input_text },'  
                         f'conversation_id is: { conversation_id }'
                         )

            stream_id = str(uuid.uuid4()) # Create a unique stream ID which will be passed back to JS and used to establish the streaming connection
            logger.debug(f'running stream_response() ... stream_id generated is: { stream_id }')

            # Store the context for this stream ID in session data
            request.session[stream_id] = { 
                'user_input': input_text,
                'conversation_id': conversation_id,
                'first_name': user.first_name,
                'timestamp': now().strftime('%H:%M, %d-%m-%Y')
            }

            # This is a check to ensure the stream_id is stored in the session
            if stream_id in request.session:
                logger.debug(f'running stream_response() ... stream_id {stream_id} successfully stored in session')
            else:
                logger.debug(f'running stream_response() ... failed to store stream_id {stream_id} in session')
            

            # Return JSON response with the stream_id
            response_data = {"stream_id": stream_id}
            logger.debug(f'Returning response: {response_data}')
            return JsonResponse(response_data)

        # If submission = POST && the form fails validation, return a JSON with an error message
        else:
            logger.debug(f'Stream response view: form validation failed: { input_form.errors }')
            return JsonResponse({'success': False, 'errors': input_form.errors}, status=400)

    
    # GET: Uses the stream_id to retrieve the stored context and streams the AI response back to the client
    elif request.method == 'GET':
        stream_id = request.GET.get('stream_id') # Get the stream_id provided by the JS
        
        # If stream_id is missing, throw an error
        if not stream_id or stream_id not in request.session:
            return JsonResponse({"error": "Invalid or missing stream ID"}, status=400)

        context = request.session.pop(stream_id) # This uses stream_id to retrieve the context stored in session
        return stream_response_to_user(
            conversation_id=context['conversation_id'],
            user_input=context['user_input'],
            user=user,
            )
    










