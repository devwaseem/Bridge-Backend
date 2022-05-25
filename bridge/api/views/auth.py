from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bridge.models import User


class ConfirmEmailApiView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uidb64",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.STR,
                required=True,
                description="base64 encoded uid",
            ),
            OpenApiParameter(
                name="token",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.STR,
                required=True,
                description="Token to confirm email",
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Successfully confirmed email",
                response=inline_serializer(
                    name="ConfirmEmailSuccessResponseSerializer",
                    fields={
                        "detail": serializers.CharField(
                            default="Your Email has been Verified."
                        ),
                    },
                ),
            ),
            410: OpenApiResponse(
                description="Link is invalid or expired.",
                response=inline_serializer(
                    name="ConfirmEmailErrorResponseSerializer",
                    fields={
                        "detail": serializers.CharField(
                            default="Link is invalid or expired."
                        ),
                    },
                ),
            ),
        },
    )
    def get(self, requst, uidb64, token):
        error_data = {"detail": "Link is invalid or expired."}
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user: User = User.objects.get(id=uid)
            verified = user.confirm_email(token)
            if verified:
                return Response(
                    {"detail": "Your Email has been Verified."},
                    status=200,
                )
            else:
                return Response(error_data, status=410)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(error_data, status=410)


class PasswordResetInitiateApiView(APIView):
    class PasswordResetInitiateRequestSerializer(serializers.Serializer):
        email = serializers.EmailField()

    permission_classes = [AllowAny]

    @extend_schema(
        request=PasswordResetInitiateRequestSerializer,
        responses={
            200: OpenApiResponse(
                description="Successfully sent password reset email",
                response=inline_serializer(
                    name="PasswordResetInitiateSuccessResponseSerializer",
                    fields={
                        "detail": serializers.CharField(
                            default="Thanks, check your email for instructions to reset your password."
                        ),
                    },
                ),
            )
        },
    )
    def post(self, request):
        serializer = self.PasswordResetInitiateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
            user.send_password_reset_email()
        except User.DoesNotExist:
            pass
        return Response(
            {
                "detail": "Thanks, check your email for instructions to reset your password.",
            },
            status=200,
        )


class PasswordResetApiView(APIView):
    class PasswordResetRequestSerializer(serializers.Serializer):
        new_password = serializers.CharField(min_length=8)

    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uidb64",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.STR,
                required=True,
                description="base64 encoded uid",
            ),
            OpenApiParameter(
                name="token",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.STR,
                required=True,
                description="Token to reset password",
            ),
        ],
        request=PasswordResetRequestSerializer,
        responses={
            200: OpenApiResponse(
                description="Successfully reset password",
                response=inline_serializer(
                    name="PasswordResetSuccessResponseSerializer",
                    fields={
                        "detail": serializers.CharField(
                            default="Your password has been reset."
                        ),
                    },
                ),
            ),
            410: OpenApiResponse(
                description="Link is invalid or expired.",
                response=inline_serializer(
                    name="PasswordResetErrorResponseSerializer",
                    fields={
                        "detail": serializers.CharField(
                            default="Link is invalid or expired."
                        ),
                    },
                ),
            ),
        },
    )
    def post(self, request, uidb64, token):
        error_data = {"detail": "Link is invalid or expired."}
        serializer = self.PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data["new_password"]
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user: User = User.objects.get(id=uid)
            reset_done = user.reset_password_using_token(
                token=token, new_password=new_password
            )
            if reset_done:
                return Response(
                    {"detail": "Your password has been reset."},
                    status=200,
                )
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            pass
        return Response(error_data, status=410)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uidb64",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.STR,
                required=True,
                description="base64 encoded uid",
            ),
            OpenApiParameter(
                name="token",
                location=OpenApiParameter.PATH,
                type=OpenApiTypes.STR,
                required=True,
                description="Token to reset password",
            ),
        ],
        request=PasswordResetRequestSerializer,
        responses={
            410: OpenApiResponse(
                description="Link is invalid or expired.",
                response=inline_serializer(
                    name="PasswordResetErrorResponseSerializer",
                    fields={
                        "detail": serializers.CharField(
                            default="Link is invalid or expired."
                        ),
                    },
                ),
            ),
        },
    )
    def get(self, request, uidb64, token):
        error_data = {"detail": "Link is invalid or expired"}
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user: User = User.objects.get(id=uid)
            print(user)
            print(PasswordResetTokenGenerator().check_token(user=user, token=token))
            if PasswordResetTokenGenerator().check_token(user=user, token=token):
                return Response(status=200)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            pass
        return Response(error_data, status=410)


class PasswordChangeApiView(APIView):
    class PasswordChangeRequestSerializer(serializers.Serializer):
        current_password = serializers.CharField(min_length=8)
        new_password = serializers.CharField(min_length=8)

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.PasswordChangeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_password = serializer.validated_data["current_password"]
        new_password = serializer.validated_data["new_password"]
        user = request.user
        reset_done = user.reset_password_using_current_password(
            current_password=current_password, new_password=new_password
        )
        if reset_done:
            return Response(
                {"detail": "Your password has been changed."},
                status=200,
            )
        return Response(
            {"detail": "Your current password is incorrect."},
            status=400,
        )


class IsAuthenticatedApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(status=200)
