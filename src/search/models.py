from django.db import models

# Create your models here.

class Search(models.Model):
    search_text = models.CharField( blank=True, max_length=255 , null=True, help_text="Search Text")
    relevance_number = models.IntegerField( null=False, help_text="Relevence Number")