from typing import Union

from django.contrib.auth import authenticate
from django.contrib.auth.base_user import AbstractBaseUser
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from bridge.models import User


class RecruiterLoginAPIView(APIView):
    class RecruiterLoginRequestSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(max_length=128)

        def validate(self, data: dict) -> dict:
            if User.objects.filter(email=data["email"]).exists():
                user: User = User.objects.get(email=data["email"])
                if not user.is_recruiter:
                    raise AuthenticationFailed("Invalid credentials")
                if not user.is_active:
                    raise AuthenticationFailed("Your account has been disabled")

                user: Union[AbstractBaseUser, AbstractBaseUser, None] = authenticate(
                    **data, request=self.context.get("request")
                )
                if user:
                    data["user"] = user
                    return data
            raise AuthenticationFailed("Invalid credentials")

    permission_classes = [AllowAny]

    @extend_schema(
        request=RecruiterLoginRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="RecruiterLoginReponse",
                    fields={
                        "token": inline_serializer(
                            name="Token",
                            fields={
                                "refresh": serializers.CharField(),
                                "access": serializers.CharField(),
                            },
                        ),
                    },
                ),
            ),
            401: {"detail": "Invalid credentials"},
        },
    )
    def post(self, request):
        serializer = self.RecruiterLoginRequestSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "token": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            }
        )
