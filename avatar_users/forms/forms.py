from avatar_users.models import UserProfile
from .custom_fields import *
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .form_fields import *
from django.utils.translation import gettext_lazy as _

import logging


logger = logging.getLogger('django')


__all__ = ['LoginForm', 'ProfileForm', 'RegistrationForm']

#------------------------------------------------------------------------

class LoginForm(forms.Form):
    email = EmailFieldLowerRegexStrict(
        label=_('Email address') + ':', 
        max_length=100,
        widget=forms.EmailInput(attrs={
            'autocomplete': 'off',
            'class': 'form-control mx-auto',
            'placeholder': _('email address'),
            })
        )

    password = forms.CharField(
        label=_('Password'),
        strip=True,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'off',
            'class': 'form-control mx-auto',
            'placeholder': _('password'),
            })
        )

#-------------------------------------------------------------------------

class ProfileForm(forms.ModelForm):
    # Fields from the User model
    first_name = first_name
    last_name = last_name
    data_source = data_source 
    response_length = response_length
    chat_history_window = chat_history_window
    top_p = top_p
    temperature = temperature
    chunk_size = chunk_size
    chunk_overlap = chunk_overlap
    langchain_k = langchain_k
    rag_sources_shown=rag_sources_shown
    rag_sources_used=rag_sources_used
    tokenization_and_vectorization_model=tokenization_and_vectorization_model
    similarity_metric=similarity_metric
    retriever_model=retriever_model

    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'data_source', 'response_length', 'chat_history_window', 
            'temperature', 'top_p', 'chunk_size', 'chunk_overlap', 'langchain_k',
            'rag_sources_shown','rag_sources_used', 'tokenization_and_vectorization_model',
            'similarity_metric', 'retriever_model'
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)

        # Initialize fields with user data
        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name

        # Initialize fields with user profile data
        self.fields['data_source'].initial = self.user.aichat_userprofile.data_source
        self.fields['response_length'].initial = self.user.aichat_userprofile.response_length
        self.fields['chat_history_window'].initial = self.user.aichat_userprofile.chat_history_window
        self.fields['temperature'].initial = self.user.aichat_userprofile.temperature
        self.fields['top_p'].initial = self.user.aichat_userprofile.top_p
        self.fields['chunk_size'].initial = self.user.aichat_userprofile.chunk_size
        self.fields['chunk_overlap'].initial = self.user.aichat_userprofile.chunk_overlap
        self.fields['langchain_k'].initial = self.user.aichat_userprofile.langchain_k
        self.fields['rag_sources_shown'].initial= self.user.aichat_userprofile.rag_sources_shown
        self.fields['rag_sources_used'].initial= self.user.aichat_userprofile.rag_sources_used
        self.fields['tokenization_and_vectorization_model'].initial = self.user.aichat_userprofile.tokenization_and_vectorization_model
        self.fields['similarity_metric'].initial = self.user.aichat_userprofile.similarity_metric
        self.fields['retriever_model'].initial = self.user.aichat_userprofile.retriever_model



    def save(self, commit=True):
        # Save user data
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        
        # Save user profile data
        user_profile = self.user.aichat_userprofile
        user_profile.data_source = self.cleaned_data['data_source']
        user_profile.response_length = self.cleaned_data['response_length']
        user_profile.chat_history_window = self.cleaned_data['chat_history_window']
        user_profile.temperature = self.cleaned_data['temperature']
        user_profile.top_p = self.cleaned_data['top_p']
        user_profile.chunk_size = self.cleaned_data['chunk_size']
        user_profile.chunk_overlap = self.cleaned_data['chunk_overlap']
        user_profile.langchain_k = self.cleaned_data['langchain_k']
        user_profile.rag_sources_shown = self.cleaned_data['rag_sources_shown']
        user_profile.rag_sources_used = self.cleaned_data['rag_sources_used']
        user_profile.tokenization_and_vectorization_model = self.cleaned_data['tokenization_and_vectorization_model']
        user_profile.similarity_metric = self.cleaned_data['similarity_metric']
        user_profile.retriever_model = self.cleaned_data['retriever_model']

        if commit:
            self.user.save()
            user_profile.save()

        return self.user
    

#-------------------------------------------------------------------------

class RegistrationForm(forms.Form):

    first_name = first_name
    last_name = last_name
    username = username
    email = email
    password = password
    password_confirmation = password_confirmation
    user_employer=user_employer


