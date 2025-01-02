from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from .models import CustomUser
from .serializers import UserSerializer

# @api_view(['POST'])
# def follow_user(request, user_id):
#     user_to_follow = User.objects.get(id=user_id)
#     request.user.following.add(user_to_follow)
#     return Response({'status': 'followed'}, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def unfollow_user(request, user_id):
#     user_to_unfollow = User.objects.get(id=user_id)
#     request.user.following.remove(user_to_unfollow)
#     return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    if user_to_follow == request.user:
        return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    if request.user.following.filter(id=user_id).exists():
        return Response({"message": "You are already following this user."}, status=status.HTTP_200_OK)

    request.user.following.add(user_to_follow)
    return Response({"message": f"You are now following {user_to_follow.username}."}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
    if not request.user.following.filter(id=user_id).exists():
        return Response({"error": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)

    request.user.following.remove(user_to_unfollow)
    return Response({"message": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)