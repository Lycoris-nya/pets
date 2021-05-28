from django.http import QueryDict, HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotAuthenticated
from rest_framework.views import APIView
from accountingForCatsAndDoqsAPI.apiKeyPermission import Check_API_KEY_Auth
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
            if isinstance(query_string["limit"], int):
                return HttpResponseBadRequest("limit mast be int")
            limit = int(query_string["limit"])
            if limit < 0:
                return HttpResponseBadRequest("limit must be non-negative")
        if "offset" in query_string:
            if isinstance(query_string["offset"], int):
                return HttpResponseBadRequest("offset mast be int")
            offset = int(query_string["offset"])
            if offset < 0:
                return HttpResponseBadRequest("offset mast be non-negative")
        if "has_photos" in query_string:
            if query_string["has_photos"] == "True" or query_string["has_photos"] == "true":
                has_photos = True
            elif query_string["has_photos"] == "False" or query_string["has_photos"] == "false":
                has_photos = False
            else:
                return HttpResponseBadRequest("has_photos mast be bool")
        return Response({"count": len(Pet.objects.all()),
                         "items": self.get_pets(has_photos=has_photos, offset=offset, limit=limit)})

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
