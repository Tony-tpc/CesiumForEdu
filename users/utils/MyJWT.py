import jwt
import datetime
from django.conf import settings
from users.models import FrontendUser

def generate_tokens(user):
    """
    生成 access_token 和 refresh_token
    """
    payload = {
        "user_id": str(user.user_id),  # 存 user_id 而不是 id
        "exp": datetime.datetime.utcnow() + settings.JWT_CONFIG["ACCESS_TOKEN_LIFETIME"],
        "iat": datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_CONFIG["ALGORITHM"])

    refresh_payload = {
        "user_id": str(user.user_id),
        "exp": datetime.datetime.utcnow() + settings.JWT_CONFIG["REFRESH_TOKEN_LIFETIME"],
        "iat": datetime.datetime.utcnow(),
    }
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm=settings.JWT_CONFIG["ALGORITHM"])

    return access_token, refresh_token


def decode_token(token):
    """
    解析 JWT 并返回 user_id
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_CONFIG["ALGORITHM"]])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None  # 令牌过期
    except jwt.InvalidTokenError:
        return None  # 令牌无效