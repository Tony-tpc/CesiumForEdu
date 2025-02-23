from django.http import JsonResponse
from neo4jDB.models import Person

def get_person(request, name):
    person = Person.nodes.get(name=name)
    return JsonResponse({"name": person.name})