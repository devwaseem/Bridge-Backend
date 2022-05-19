from rest_framework import serializers
from rest_framework.views import APIView

from bridge.models import CandidateProfile

# step 1: - get the neccessary information: name, phone, city, industry, department, experience, education, resume

# step 2: - get skills from the user

# step 3: - Get the user's picture


class CandidateOnboardingStep1(APIView):
    class CandidateOnboardingStep1Serializer(serializers.ModelSerializer):

        fullname = serializers.CharField(max_length=100)

        class Meta:
            model = CandidateProfile
            fields = [
                "fullname",
                "gender",
                "date_of_birth",
                "specialization",
                "department",
                "employment_type",
                "education_type",
            ]

    def post(self, request):
        pass
