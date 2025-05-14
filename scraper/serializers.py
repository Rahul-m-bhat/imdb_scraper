from rest_framework import serializers
from .models import MovieDB

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDB
        fields = '__all__' # Expose all fields of the Movie model