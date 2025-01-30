from rest_framework.response import Response

from accounts.serializers import UserSerializer
from accounts.views.base import Base


class Signup(Base):
    def post(self, request):
        user_data = {
            'name': request.data.get('name'),
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'type_account': request.data.get('type_account', 'owner'),
            'company_id': request.data.get('company_id'),
            'company_name': request.data.get('company_name'),
            'document': request.data.get('document'),
        }
        user = self.create_user(**user_data)
        enterprise = self.get_enterprise_user(user.pk)

        serializer = UserSerializer(user).data

        return Response({
            'data': {
                'user': serializer,
                'enterprise': enterprise,
            }
        })
