from rest_framework import serializers

from .models import Pet, Photo


class PhotoSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'url': instance.url
        }

    class Meta:
        model = Photo
        fields = ('id', 'pet', 'url', 'image')

    def create(self, validated_data):
        return Photo.objects.create(**validated_data)

    def get_url(self, obj):
        return "hfbfhf"


def get_photos(obj):
    return [PhotoSerializer(obj.photo_set, many=True)]


class PetSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = ('id', 'name', 'age', 'type', 'photos', 'created_at')

    def create(self, validated_data):
        return Pet.objects.create(**validated_data)

    def get_photos(self, obj):
        g = PhotoSerializer(obj.photo_set.all(), many=True)
        return g.data

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%dT%H:%M:%S")
