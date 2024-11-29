from rest_framework import serializers
from users.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','email','password','address','phone_number']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        user = User(
            name=validated_data['name'],
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number'),
            address=validated_data.get('address'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid login credentials.')
        else:
            raise serializers.ValidationError('Both "email" and "password" are required.')
        data['user'] = user
        return data

    
