from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    ListField
    )

from . models import Search
User = get_user_model()

class SingleSearchSerializer(ModelSerializer):
    class Meta:        
        model = Search
        fields = "__all__"

class MultipleSearchSerializer(ModelSerializer):
    search_text = ListField()
    class Meta:        
        model = Search
        fields = "__all__"