from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields =["username" , "email" , "password" , "role"]
        extra_kwargs = {
        'password': {'write_only': True}
    } 

    def create(self,validated_data):
        user = CustomUser.objects.create_user(
            username= validated_data["username"],
            email= validated_data["email"],
            password= validated_data["password"],
            role= validated_data["role"],
        )
        return user 
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username" , "password"]

    def validate(self,data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(
        username=username ,
        password = password
        )    
        if user is  None:
            raise serializers.ValidationError(
                "invalid username or password"
            )
        data["user"]=user
        return data
