from django.urls import path
from .views import proxy_image, bilibili, stream_llm_response

app_name = 'proxy'
urlpatterns = [
    path('proxy-image/', proxy_image, name='proxy-image'),
    path('bilibili/', bilibili, name='bilibili'),
    path('chat/', stream_llm_response, name='stream_chat'),
]
