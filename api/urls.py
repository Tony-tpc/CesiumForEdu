from django.urls import path
from .views import chat_completion

urlpatterns = [
    path('api/chat/', chat_completion),  # 访问此端点来调用 API
]