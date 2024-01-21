import json

from django.http import JsonResponse, HttpResponse

locs = [
    {
        "rows": [
            [4, 4, 4],
            [2, 2, 2, 2, 2, 2],
            [8, 4]
        ]
    }
]
def locations(request):

    return JsonResponse({"locations": locs}, safe=False)

def location(request,id):
    location = locs[id-1]
    html = ""
    for row in location['rows']:
        html += "<div class='container-fluid pt-4 px-4'>"
        for col in row:
            html += f"<div class='col-{col}'>"
            html += f"{col}</div>"
        html += "</div>"
    return JsonResponse({"html": html}, safe=False)