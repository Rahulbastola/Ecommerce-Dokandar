from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import RegisterSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import LoginSerializer


@api_view(['POST'])
def register(request):
    Serializer =RegisterSerializer(data=request.data)
    if Serializer.is_valid():
        user=Serializer.save()

        return Response({
              "message":"register api is working"

            })
    return Response(Serializer.errors, status=400)

@api_view(['POST'])
def login(request):
    Serializer = LoginSerializer(data=request.data)
    if Serializer.is_valid():
        user= Serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })
    return Response(
        Serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )