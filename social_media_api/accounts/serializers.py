from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)
    bio = serializers.CharField(required=False)
    followers = serializers.PrimaryKeyRelatedField(many=True,
       queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers']




