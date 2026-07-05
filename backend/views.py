from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Application, Job
from .serializers import ApplicationSerializer, JobsSerializer, RegisterSerializer


@api_view(['GET'])
def hello_api(request):
    return Response({"message": "Hello from Django API"})


@csrf_exempt
@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User Registered Successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def basic_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"message": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        return Response({"user_id": user.id, "username": user.username, "message": "Login successful"}, status=status.HTTP_200_OK)

    return Response({"message": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def job_list(request):
    jobs = Job.objects.all()
    serializer = JobsSerializer(jobs, many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def apply_job(request):
    serializer = ApplicationSerializer(data=request.data)
    job_id = request.data.get("job")
    applicant_id = request.data.get("applicant")

    if not job_id or not applicant_id:
        return Response({"message": "Job and applicant are required."}, status=status.HTTP_400_BAD_REQUEST)

    if not Job.objects.filter(id=job_id).exists():
        return Response({"message": "Selected job does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    if not User.objects.filter(id=applicant_id).exists():
        return Response({"message": "Selected applicant does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    if Application.objects.filter(job_id=job_id, applicant_id=applicant_id).exists():
        return Response({"message": "You already have applied!"}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Application submitted"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
