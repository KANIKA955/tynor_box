from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Design, CDR, BoxDesign

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']  # Include only necessary fields

    def validate_email(self, value):
        """
        Ensure email is unique for user registration.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        """
        Override create method to hash password before saving the user.
        """
        password = validated_data.get('password')
        if password:
            validated_data['password'] = User.objects.make_random_password()  # This should be replaced if you are not generating random passwords.
        user = super().create(validated_data)
        user.set_password(password)  # Make sure password is hashed before saving
        user.save()
        return user


# Serializer for Design model
class DesignSerializer(serializers.ModelSerializer):
    """
    Serializer for the Design model
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)  # Allow user to be passed if needed

    class Meta:
        model = Design
        fields = '__all__'  # Includes all fields from the Design model


# Serializer for CDR model
class CDRSerializer(serializers.ModelSerializer):
    """
    Serializer for the CDR model
    """
    design = serializers.PrimaryKeyRelatedField(queryset=Design.objects.all())  # Accepts design ID
    generated_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Accepts user ID

    class Meta:
        model = CDR
        fields = ['id', 'design', 'generated_by', 'specifications', 'approval_status', 'generated_at']

    def validate(self, data):
        """
        Custom validation for CDR to ensure design and user exist.
        """
        if not data.get('design'):
            raise serializers.ValidationError("Design must be specified.")
        if not data.get('generated_by'):
            raise serializers.ValidationError("User must be specified.")
        return data

    def create(self, validated_data):
        """
        Override the create method to associate the correct design and user before saving the CDR.
        """
        design = validated_data['design']
        generated_by = validated_data['generated_by']
        specifications = validated_data['specifications']
        approval_status = validated_data.get('approval_status', 'Pending')

        # Ensure design and user exist and validate them if necessary
        if not design:
            raise serializers.ValidationError("Design must be specified.")
        if not generated_by:
            raise serializers.ValidationError("User must be specified.")

        # Create the CDR instance
        cdr = CDR.objects.create(
            design=design,
            generated_by=generated_by,
            specifications=specifications,
            approval_status=approval_status
        )
        return cdr


# Serializer for BoxDesign model
class BoxDesignSerializer(serializers.ModelSerializer):
    """
    Serializer for the BoxDesign model with all fields mapped.
    """
    logo = serializers.ImageField(required=False, allow_null=True)  # Logo as an optional image field

    class Meta:
        model = BoxDesign
        fields = ['width', 'height', 'depth', 'material', 'text', 'logo']  # Include all the relevant fields

    def validate(self, data):
        """
        Validate box design fields for logical correctness.
        """
        # Validate width, height, and depth are greater than 0
        if data.get('width') and data['width'] <= 0:
            raise serializers.ValidationError("Width must be greater than 0.")
        if data.get('height') and data['height'] <= 0:
            raise serializers.ValidationError("Height must be greater than 0.")
        if data.get('depth') and data['depth'] <= 0:
            raise serializers.ValidationError("Depth must be greater than 0.")
        
        # Optionally validate the logo (e.g., check if it's a valid image)
        if data.get('logo'):
            if not data['logo'].name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise serializers.ValidationError("Logo must be a PNG, JPG, or JPEG image.")
        
        return data


# Custom Token Obtain Pair serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom Token Obtain Pair serializer to include custom fields in the response.
    """
    @classmethod
    def get_token(cls, user):
        # Get the default token
        token = super().get_token(user)
        
        # Add custom claims to the token
        token['username'] = user.username
        token['role'] = user.role
        token['email'] = user.email  # Include email in the token
        return token

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()