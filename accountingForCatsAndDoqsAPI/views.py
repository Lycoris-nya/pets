from django.http import QueryDict, HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotAuthenticated
from rest_framework.views import APIView
from accountingForCatsAndDoqsAPI.api_key_permission import Check_API_KEY_Auth
from .models import Pet
from .serializers import PetSerializer, PhotoSerializer
from .query_string_parser import parse_query_string


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
        query_string = parse_query_string(QueryDict(request.META["QUERY_STRING"]))
        if 'error' in query_string:
            return query_string["error"]
        return Response({"count": len(Pet.objects.all()),
                         "items": self.get_pets(has_photos=query_string["has_photos"], offset=query_string["offset"],
                                                limit=query_string["limit"])})

    def post(self, request):
        pet = request.data
        serializer = PetSerializer(data=pet)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        errors = []
        if 'ids' not in request.data:
            raise ParseError("Empty content")
        pets = Pet.objects.all().filter(id__in=request.data["ids"])
        deleted_pet_id = [str(pet.id) for pet in pets]
        deleted = pets.delete()
        deleted_count = 0
        if deleted[0] != 0:
            deleted_count = deleted[1]["accountingForCatsAndDoqsAPI.Pet"]
        for pet_id in request.data["ids"]:
            if pet_id not in deleted_pet_id:
                errors.append({"id": pet_id, "error": "Pet with the matching ID was not found."})
        return Response({"deleted": deleted_count, "errors": errors})


class PhotoView(APIView):
    permission_classes = (Check_API_KEY_Auth,)

    def post(self, request, pk):
        if 'file' not in request.data:
            raise ParseError("Empty content")
        data = {"pet": pk, "image": request.data['file']}
        serializer = PhotoSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
