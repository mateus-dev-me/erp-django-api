from rest_framework.views import Response

from accounts.auth import get_token
from accounts.serializers import UserSerializer

from .base import Base


class Signin(Base):
    def post(self, request) -> Response:
        email = request.data.get('email')
        password = request.data.get('password')

        self.validate_not_null(email=email, password=password)

        user = self.get_user(email, password)
        token_data = get_token(user)

        enterprise = self.get_enterprise_user(user.id)

        user_data = UserSerializer(user).data

        return Response({
            'data': {
                'user': user_data,
                'enterprise': enterprise,
                'token': token_data,
            },
        })
