"""
    search URL Configuration

"""
from django.contrib import admin
from django.urls import path,include

from .views import SearchSingleText,SearchMultipleText
urlpatterns = [
    path('searchSingleText/', SearchSingleText.as_view() , name = 'search-single-text'),
    path('multipleSearchText/', SearchMultipleText.as_view(), name = 'multiple-search-text')
]
