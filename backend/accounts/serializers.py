from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.mail import send_mail
import random

from .models import User, PasswordResetOTP



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'password',
            'confirm_password'
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User.objects.create_user(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        return user



# LOGIN (NO USER IN RESPONSE)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            email=data.get('email'),
            password=data.get('password')
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        # internal use only (view will create JWT)
        self.user = user
        return data


#----- SEND OTP-----

class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        if not User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError("User not found")
        return data

    def save(self):
        otp = str(random.randint(100000, 999999))
        PasswordResetOTP.objects.create(
            email=self.validated_data["email"],
            otp=otp
        )

        send_mail(
            "SmartPark Password Reset OTP",
            f"Your OTP is {otp}. Valid for 5 minutes.",
            None,
            [self.validated_data["email"]],
        )



#---- VERIFY OTP & RESET PASSWORD----

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=6)

    def save(self):
        record = PasswordResetOTP.objects.filter(
            email=self.validated_data["email"],
            otp=self.validated_data["otp"]
        ).last()

        if not record or record.is_expired():
            raise serializers.ValidationError("Invalid or expired OTP")

        user = User.objects.get(email=record.email)
        user.set_password(self.validated_data["new_password"])
        user.save()
        record.delete()
