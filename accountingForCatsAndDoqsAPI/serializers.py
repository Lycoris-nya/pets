from rest_framework import serializers

from .models import Pet, Photo


class PhotoSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'url': instance.image.url
        }

    class Meta:
        model = Photo
        fields = ('id', 'pet', 'url', 'image')

    def create(self, validated_data):
        return Photo.objects.create(**validated_data)

    def get_url(self, obj):
        return obj.image.url


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

    def validate_type(self, value):
        if value != "cat" and value != "dog":
            raise serializers.ValidationError("Type can only be a cat or a dog")
        return value
    def validate_age(self, value):
        if value < 0:
            raise serializers.ValidationError("Age must be non-negative")
        return value
