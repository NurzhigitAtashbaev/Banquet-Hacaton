from rest_framework import serializers

from restaurants.serializers import RestaurantSerializer
# from django.contrib.auth import get_user_model
from .models import CustomUser
from .send_email import send_activation_code, send_reset_password_code


# User = get_user_model()  # CustomUser

class AccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = '__all__'
    
class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'avatar')

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        required=True,
        min_length=6,
        write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2', 'avatar', 'first_name', 'last_name', 'username')

    def validate_email(self, email):
        return email

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password2')

        if p1 != p2:
            raise serializers.ValidationError('Password did not match!!!')

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        send_activation_code(user.email, user.activation_code)
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('пользователь с такой почтой не существует')
        return email

    def send_reset_password_code(self):
        email = self.validated_data.get('email')
        user = CustomUser.objects.get(email=email)
        user.create_activation_code()
        user.save()
        send_reset_password_code(email=email, code=user.activation_code)


class ForgotPasswordComleteSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, min_length=6)
    password_confirm = serializers.CharField(required=True, min_length=6)
    code = serializers.CharField(required=True)

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.get('password_confirm')
        if p1 != p2:
            raise serializers.ValidationError('пароли не совпадают')
        return attrs

    def validate_code(self, code):
        if not CustomUser.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('неверный код')
        return code

    def set_new_password(self):
        user = CustomUser.objects.get(activation_code=self.validated_data.get('code'))
        password = self.validated_data.get('password')
        user.set_password(password)
        user.activation_code = ''
        user.save(update_fields=['password', 'activation_code'])


class UserSerializer(serializers.ModelSerializer):
    favorites = RestaurantSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'favorites']
