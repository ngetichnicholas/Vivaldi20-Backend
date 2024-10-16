from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import (
    UserRegistrationView, LoginView, LogoutView,
    ListMembersView, MemberDetailView, UpdateProfilePhotoView
)

schema_view = get_schema_view(
    openapi.Info(
        title="Vivaldi Channel API",
        default_version='v1',
        description="API documentation for Vivaldi Channel App",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),

)


urlpatterns = [
    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # User authentication endpoints
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # User registration
    path('register/', UserRegistrationView.as_view(), name='register'),

    # Member management
    path('members/', ListMembersView.as_view(), name='list-members'),
    path('members/<int:pk>/', MemberDetailView.as_view(), name='member-detail'),
    path('members/<int:id>/update-profile-photo/', UpdateProfilePhotoView.as_view(), name='update-profile-photo'),

]
