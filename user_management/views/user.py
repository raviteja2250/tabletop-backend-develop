""" Declear class-based view for exposing User model """

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from rest_framework_simplejwt.authentication import JWTAuthentication

from user_management.models import User
from user_management.serializers import UserSerializer


class UserViewSet(APIView):
    """ User viewset """

    permission_classes = []
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()

    def put(self, request):
        if request.user.is_anonymous:
            return Response({}, status=HTTP_200_OK)

        serializer = UserSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
