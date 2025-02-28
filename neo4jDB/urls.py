from django.urls import path
from .views import get_graph

app_name = "neo4jDB"
urlpatterns = [
    path('get-graph/', get_graph, name='get_graph'),
]
