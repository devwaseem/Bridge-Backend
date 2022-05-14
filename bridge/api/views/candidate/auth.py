from typing import Union

from django.contrib.auth import authenticate
from django.contrib.auth.base_user import AbstractBaseUser
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from bridge.models import Candidate, User


class CandidateLoginAPIView(APIView):
    class CandidateLoginRequestSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(max_length=128)

        def validate(self, data: dict) -> dict:
            user: Union[AbstractBaseUser, AbstractBaseUser, None] = authenticate(
                **data, role=User.Role.CANDIDATE, request=self.context.get("request")
            )
            if user and user.is_active:
                data["user"] = user
                return data
            raise AuthenticationFailed("Invalid credentials")

    permission_classes = [AllowAny]

    @extend_schema(
        request=CandidateLoginRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="CandidateLoginReponse",
                    fields={
                        "token": inline_serializer(
                            name="Token",
                            fields={
                                "refresh": serializers.CharField(),
                                "access": serializers.CharField(),
                            },
                        ),
                        "signup_step": serializers.IntegerField(),
                    },
                ),
            ),
            401: {"detail": "Invalid credentials"},
        },
    )
    def post(self, request):
        serializer = self.CandidateLoginRequestSerializer(
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
                "signup_step": user.signup_step,
            }
        )


class CandidateSignupAPIView(APIView):
    class CandidateSignupRequestSerializer(serializers.Serializer):
        email = serializers.EmailField(
            validators=[
                UniqueValidator(
                    queryset=User.objects.all(), message="Email already exists"
                )
            ]
        )
        password = serializers.CharField(max_length=128)

    permission_classes = [AllowAny]

    @extend_schema(
        request=CandidateSignupRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="CandidateSignupReponse",
                    fields={
                        "detail": serializers.CharField(),
                    },
                )
            ),
        },
    )
    def post(self, request):
        serializer = self.CandidateSignupRequestSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        Candidate.objects.create_candidate(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        return Response({"detail": "Signup successful"})
