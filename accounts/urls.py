from django.urls import path

from .views import (
    register_user,
    get_me,
    list_users,
    create_user,
    update_role,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('register/', register_user),

    path('login/', TokenObtainPairView.as_view()),

    path('refresh/', TokenRefreshView.as_view()),

    path('me/', get_me),

    path('users/', list_users),

    path('users/create/', create_user),

    path(
    'users/<int:user_id>/role/',
    update_role
),

]