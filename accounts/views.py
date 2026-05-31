from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer


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