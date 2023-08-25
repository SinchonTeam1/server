from rest_framework import serializers
from users.models import User
from .models import Study, StudyFavorite

class StudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = '__all__'


class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']


class StudyGetSerializer(StudySerializer):
    writer = WriterSerializer()
    members = WriterSerializer(many=True)
    class Meta(StudySerializer.Meta):
        pass

class StudyFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyFavorite
        fields = '__all__'