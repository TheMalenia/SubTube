from rest_framework import serializers
from .models import User, Video, SubscriptionType, Subscription, History
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'wallet', 'renewal']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class SubscriptionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionType
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'


class PasswordConfirmationMixin:
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Password fields did not match.'})

        return data


class SignUpSerializer(
    PasswordConfirmationMixin,
    serializers.ModelSerializer,
):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password2',
            'email',
            # 'first_name',
            # 'last_name',
        )
        # extra_kwargs = {
        #     'first_name': {
        #         'required': True,
        #     },
        #     'last_name': {
        #         'required': True,
        #     },
        # }

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            # first_name=validated_data['first_name'],
            # last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user



