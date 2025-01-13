from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='avatar_userprofile')
    user_employer = models.CharField(max_length=100, null=True, blank=True, default='Kebayoran Technologies')
    data_source = models.CharField(max_length=64, null=True, blank=True, default='all')
    response_length = models.IntegerField(null=True, blank=True, default=4, validators=[MinValueValidator(1), MaxValueValidator(200)])
    chat_history_window = models.IntegerField(null=True, blank=True, default=5, validators=[MinValueValidator(0), MaxValueValidator(200)])
    temperature = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=0.30, validators=[MinValueValidator(0.00), MaxValueValidator(1.00)])
    top_p = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=1.0, validators=[MinValueValidator(0.00), MaxValueValidator(1.00)])
    chunk_size = models.IntegerField(default=1000, validators=[MinValueValidator(100), MaxValueValidator(30000)], null=True, blank=True)
    chunk_overlap = models.DecimalField(max_digits=2, decimal_places=2, default=.30, validators=[MinValueValidator(0.00), MaxValueValidator(.75)], null=True, blank=True)
    langchain_k = models.IntegerField(null=True, blank=True, default=5, validators=[MinValueValidator(0), MaxValueValidator(20)])
    rag_sources_shown = models.CharField(max_length=100, null=True, blank=True, default='all') # Can be 'website', 'document' or 'all'
    rag_sources_used = models.CharField(max_length=100, null=True, blank=True, default='all') # Can be 'website', 'document' or 'all'
    tokenization_and_vectorization_model = models.CharField(max_length=100, null=True, blank=True, default='bert-base-multilingual-cased')
    preprocessing_model = models.CharField(max_length=100, null=True, blank=True, default='en_core_web_sm')
    similarity_metric = models.CharField(max_length=100, null=True, blank=True, default='cosine')
    retriever_model = models.CharField(max_length=100, null=True, blank=True, default='gpt-4o-mini')
    preprocessing = models.BooleanField(null=True, blank=True, default=False)
    conversation_id = models.CharField(null=True, blank=True, max_length=200)


    class Meta:
        db_table = 'avatar_userprofile'  # Rename the table here

    def __str__(self):
        return f"{self.user.username}'s Profile"