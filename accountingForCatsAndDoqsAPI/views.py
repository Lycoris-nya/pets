from django.http import QueryDict, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from django import forms
from urllib.parse import parse_qs
from django.db.models import Q
from accountingForCatsAndDoqsAPI.apiKeyPermission import Check_API_KEY_Auth
from accountingForCatsAndDogs.settings import BASE_DIR, DATABASES
from .models import Photo
from rest_framework.parsers import FileUploadParser
from django.http import HttpResponse

from .models import Pet
from .serializers import PetSerializer, PhotoSerializer


class PetView(APIView):
    permission_classes = (Check_API_KEY_Auth,)

    def permission_denied(self, request, message=None, code=None):
        raise NotAuthenticated()

    def get_pets(self, has_photos=None, offset=0, limit=None):
        if limit is None:
            limit = len(Pet.objects.all())
        pets = Pet.objects.all()[offset:]
        if has_photos is not None:
            list_of_ids = []
            for pet in pets:
                photo_count = len(pet.photo_set.all())
                if has_photos is True and photo_count > 0:
                    list_of_ids.append(pet.id)
                if has_photos is False and photo_count == 0:
                    list_of_ids.append(pet.id)
            pets = Pet.objects.all().filter(id__in=list_of_ids)
        return PetSerializer(pets[:limit], many=True).data

    def get(self, request):
        query_string = QueryDict(request.META["QUERY_STRING"])
        limit = 20
        offset = 0
        has_photos = None
        if "limit" in query_string:
            limit = int(query_string["limit"])
        if "offset" in query_string:
            offset = int(query_string["offset"])
        if "has_photos" in query_string:
            if query_string["has_photos"] == "True" or query_string["has_photos"] == "true":
                has_photos = True
            else:
                has_photos = False
        return Response({"count": len(Pet.objects.all()), "items": self.get_pets(has_photos = has_photos, offset=offset,limit = limit)})

    def post(self, request):
        pet = request.data
        serializer = PetSerializer(data=pet)
        if serializer.is_valid(raise_exception=True):
            if request.data["type"] != "cat" and request.data["type"] != "dog":
                return HttpResponseBadRequest("Type can only be a cat or a dog")
            serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        deleted = 0
        deleted_pet_id = []
        errors = []
        if 'ids' not in request.data:
            raise ParseError("Empty content")
        pets = Pet.objects.all().filter(id__in=request.data["ids"])
        for pet in pets:
            deleted += 1
            for photo in pet.photo_set.all():
                photo.image.delete(save=True)
                photo.delete()
            deleted_pet_id.append(pet.id)
            pet.delete()
        for pet_id in request.data["ids"]:
            if pet_id not in deleted_pet_id:
                errors.append({"id": pet_id, "error": "Pet with the matching ID was not found."})
        return Response({"deleted": deleted, "errors": errors})


class ImageUploadParser(FileUploadParser):
    media_type = 'image/*'


class PhotoView(APIView):
    permission_classes = (Check_API_KEY_Auth,)

    parser_class = (FileUploadParser, ImageUploadParser,)

    def post(self, request, pk):
        if 'file' not in request.data:
            raise ParseError("Empty content")
        dat = {"pet": pk, "image": request.data['file'],
               "url": "http://" + str(BASE_DIR) + "/photos/" + request.data['file'].name}
        serializer = PhotoSerializer(data=dat)
        if serializer.is_valid(raise_exception=True):
            photo_saved = serializer.save()
        return Response({"id": photo_saved.id, "url": photo_saved.url})
