from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from drf_yasg.utils import swagger_auto_schema
from django.utils.translation import gettext as _
from .serializers import UserRegistrationSerializer, UserSerializer
from .models import User


# User Registration View (Function Based)
@swagger_auto_schema(method='post', request_body=UserRegistrationSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"data": {"message": "User account created successfully"}}, status=status.HTTP_201_CREATED)
    return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Login View (Function Based)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = ObtainAuthToken.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({
            "data": {
                "message": "User with that Email or Phone does not exist.",
                "errors": {
                    "username": ["User with that Email or Phone does not exist."]
                }
            }
        }, status=422)

    if not user.check_password(password):
        return Response({
            "data": {
                "message": "The password entered is invalid.",
                "errors": {
                    "password": ["The password entered is invalid."]
                }
            }
        }, status=422)

    token, created = Token.objects.get_or_create(user=user)

    return Response({
        "data": {
            "user": {
                "id": user.id,
                "name": user.first_name,
                "username": user.username,
                "profession": user.profession,
                "profile_photo_url": user.profile_photo.url if user.profile_photo else None
            },
            "token": token.key
        }
    }, status=status.HTTP_200_OK)

# Logout View (Function Based)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()
        return Response({"data": {"message": "Successfully logged out."}}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"data": {"message": "Token not found."}}, status=status.HTTP_400_BAD_REQUEST)

# List Members View (Function Based)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_members_view(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({
        "data": {
            "members": serializer.data
        }
    }, status=status.HTTP_200_OK)

# Member Detail View with CRUD operations (Function Based)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def member_detail_view(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"message": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response({"data": serializer.data})

    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = UserSerializer(user, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": {
                    "message": "Member updated successfully",
                    "member": serializer.data
                }
            })
        return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response({"data": {"message": "User deleted successfully"}})

# Update Profile Photo View (Function Based)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_photo_view(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"data": {"message": "User not found"}}, status=status.HTTP_404_NOT_FOUND)

    if 'profile_photo' in request.FILES:
        user.profile_photo = request.FILES['profile_photo']
        user.save()
        serializer = UserSerializer(user)
        response_data = {
            "data": {
                "message": "Profile photo updated successfully",
                "member": serializer.data  # This contains the updated member details
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

    return Response({"data": {"message": "No photo provided."}}, status=status.HTTP_400_BAD_REQUEST)
