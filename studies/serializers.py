from rest_framework import serializers
from .models import Study, StudyFavorite

class StudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = '__all__'

class StudyFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyFavorite
        fields = '__all__'