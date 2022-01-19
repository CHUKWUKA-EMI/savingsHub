
from rest_framework import serializers

from users.models import User

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'country','password', 'date_of_birth', 'phone_number', 'home_address','gender','employment_status')
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email','username','password', 'token')
        read_only_fields = ['token']

