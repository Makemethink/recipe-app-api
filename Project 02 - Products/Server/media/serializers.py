from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# UniqueTogetherValidator, UniqueForDateValidator, UniqueForMonthValidator, UniqueForYearValidator
from .models import Media


class ListMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = [
            'id',
            'show_name',
        ]


class ListAllMediaSerializer(serializers.ModelSerializer):

    # Unique Movie / Series / Anime name only
    show_name = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=Media.objects.all())])
    show_desc = serializers.CharField(max_length=512)

    @staticmethod
    def validate_show_desc(value):
        # Custom validation for email field
        if '--' == value:
            raise serializers.ValidationError("We don't accept -- in description")
        return value

    # The name and description of the show should not be the same
    def validate(self, data):
        # Custom validation across fields
        if 'show_name' in data and 'show_desc' in data:
            if data['show_name'].lower() == data['show_desc'].lower():
                raise serializers.ValidationError("Show name and show desc should not be the same")
        return data

    class Meta:
        model = Media
        fields = '__all__'
