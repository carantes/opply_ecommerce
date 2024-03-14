from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator

from api.identity.models import Customer

# Login user serializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Get public_id
        public_id = Customer.objects.get(username=user).public_id
        
        # Add custom claims
        token['email'] = user.email
        token['public_id'] = str(public_id)
        # ...
        
        return token
    
    
# Register user serializer
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Customer.objects.all())]
    )

    class Meta:
        model = Customer
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = Customer.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


# Customer Serializer
class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Customer
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'url', 'public_id']