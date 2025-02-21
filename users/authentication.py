from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.utils.MyJWT import decode_token
from users.models import FrontendUser

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        解析请求头中的 JWT 令牌
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]  # 提取 token
        user_id = decode_token(token)
        if not user_id:
            raise AuthenticationFailed("无效或过期的 Token")

        try:
            user = FrontendUser.objects.get(user_id=user_id)
            return user, None
        except FrontendUser.DoesNotExist:
            raise AuthenticationFailed("用户不存在")