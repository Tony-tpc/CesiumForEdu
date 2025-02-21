from rest_framework import serializers
from .models import FrontendUser

class FrontendUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)  # 头像字段为可选项

    class Meta:
        model = FrontendUser
        fields = ["user_id", "username", "email", "password", "gender","grade","remarks","correct_problems","avatar","created_at"]
        extra_kwargs = {"password": {"write_only": True,"required":True}}  # 密码不能被读取
