from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer
from .permissions import IsAdmin
from .serializers import CreateUserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    user = request.user

    try:
        role = user.profile.role
    except Exception:
        role = 'sales'

    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': role,
    })


@api_view(['GET', 'POST'])
def register_user(request):

    if request.method == 'GET':
        return Response({
            "message": "Send POST request to register"
        })

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# NEW FUNCTION
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def list_users(request):

    users = User.objects.all()

    data = []

    for user in users:

        role = getattr(user.profile, 'role', 'sales')

        data.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": role
        })

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def create_user(request):

    serializer = CreateUserSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data,
            status=201
        )

    return Response(
        serializer.errors,
        status=400
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdmin])
def update_role(request, user_id):

    try:
        user = User.objects.get(id=user_id)

        role = request.data.get("role")

        user.profile.role = role

        user.profile.save()

        return Response({
            "message": "Role updated"
        })

    except User.DoesNotExist:

        return Response(
            {"error": "User not found"},
            status=404
        )