import os
from django.utils import timezone
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from django.utils.translation import gettext as _
from .serializers import UserRegistrationSerializer, UserSerializer
from .models import User
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser

# User Registration View (Class Based)
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": {"message": "User account created successfully."}}, status=status.HTTP_201_CREATED)
        return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Login View (Class Based)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                "data": {
                    "message": "Both username and password are required.",
                    "errors": {
                        "username": ["This field is required."],
                        "password": ["This field is required."]
                    }
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({
                "data": {
                    "message": "User with that username does not exist.",
                    "errors": {"username": ["User with that username does not exist."]}
                }
            }, status=422)

        if not user.check_password(password):
            return Response({
                "data": {
                    "message": "The password entered is invalid.",
                    "errors": {"password": ["The password entered is invalid."]}
                }
            }, status=422)

        # Create or retrieve the token
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


# Logout View (Class Based)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"data": {"message": "Successfully logged out."}}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"data": {"message": "Token not found."}}, status=status.HTTP_400_BAD_REQUEST)


# List Members View (Class Based)
class ListMembersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# Member Detail View with CRUD operations (Class Based)
class MemberDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"message": "Member not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        return self._update_member(request, pk, partial=False)

    def patch(self, request, pk):
        return self._update_member(request, pk, partial=True)

    def _update_member(self, request, pk, partial):
        user = self.get_object(pk)
        if user is None:
            return Response({"message": "Member not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": {
                    "message": "Member updated successfully.",
                    "member": serializer.data
                }
            }, status=status.HTTP_200_OK)
        return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response({"message": "Member not found."}, status=status.HTTP_404_NOT_FOUND)

        # Delete the existing profile photo if it exists before deleting the user
        if user.profile_photo:
            try:
                default_storage.delete(user.profile_photo.name)
            except Exception as e:
                return Response({"data": {"message": "Error deleting profile photo"}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Now delete the user
        user.delete()
        return Response({"data": {"message": "User deleted successfully."}}, status=status.HTTP_200_OK)

# Update Profile Photo View (Class Based)
class UpdateProfilePhotoView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"data": {"message": "User not found."}}, status=status.HTTP_404_NOT_FOUND)

        if 'profile_photo' in request.FILES:
            # Delete the existing profile photo if it exists using the storage backend
            if user.profile_photo:
                try:
                    # Check if the file exists and delete it using the storage backend's name
                    default_storage.delete(user.profile_photo.name)
                except Exception as e:
                    return Response({"data": {"message": "Error updating profile photo"}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Get the uploaded file
            uploaded_file = request.FILES['profile_photo']

            # Generate the new file name using user's name and current time
            current_time = timezone.now().strftime("%Y%m%d%H%M%S")
            user_name = user.username.replace(" ", "_")  # or use another unique field like email
            file_extension = os.path.splitext(uploaded_file.name)[1]
            new_file_name = f"{user_name}_profile_{current_time}{file_extension}"

            # Save the new file with the generated name
            user.profile_photo.save(new_file_name, uploaded_file)

            # Save the user object with the new profile photo
            user.save()
            serializer = UserSerializer(user)
            response_data = {
                "data": {
                    "message": "Profile photo updated successfully.",
                    "member": serializer.data  # This contains the updated member details
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response({"data": {"message": "No photo provided."}}, status=status.HTTP_400_BAD_REQUEST)
