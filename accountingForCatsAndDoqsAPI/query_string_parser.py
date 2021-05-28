from django.http import QueryDict, HttpResponseBadRequest


def parse_query_string(query_string):
    limit = 20
    offset = 0
    has_photos = None
    if "limit" in query_string:
        if not is_int(query_string["limit"]):
            return {"error": HttpResponseBadRequest("limit mast be int")}
        limit = int(query_string["limit"])
        if limit < 0:
            return {"error": HttpResponseBadRequest("limit must be non-negative")}
    if "offset" in query_string:
        if not is_int(query_string["offset"]):
            return {"error": HttpResponseBadRequest("offset mast be int")}
        offset = int(query_string["offset"])
        if offset < 0:
            return {"error": HttpResponseBadRequest("offset mast be non-negative")}
    if "has_photos" in query_string:
        if query_string["has_photos"] == "True" or query_string["has_photos"] == "true":
            has_photos = True
        elif query_string["has_photos"] == "False" or query_string["has_photos"] == "false":
            has_photos = False
        else:
            return {"error": HttpResponseBadRequest("has_photos mast be bool")}
    return {"limit": limit, "offset": offset, "has_photos": has_photos}


def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False
