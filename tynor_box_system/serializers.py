from rest_framework import serializers
from .models import Design, CDR
from .models import ApprovalStatus  # Import the enum for approval status

class DesignSerializer(serializers.ModelSerializer):
    # Adding choices for approval status as a serializer field
    approval_status = serializers.ChoiceField(choices=ApprovalStatus.choices(), default=ApprovalStatus.PENDING.value)

    class Meta:
        model = Design
        fields = ['id', 'name', 'version', 'dimensions', 'material_specs', 'approval_status', 'created_at', 'updated_at', 'user']

    # Optional: To include a user-friendly display for the approval status
    def validate_approval_status(self, value):
        if value not in ApprovalStatus.__members__:
            raise serializers.ValidationError(f"{value} is not a valid approval status.")
        return value


class CDRSerializer(serializers.ModelSerializer):
    # Adding choices for approval status as a serializer field
    approval_status = serializers.ChoiceField(choices=ApprovalStatus.choices(), default=ApprovalStatus.PENDING.value)
    
    # To include the design's name in the CDR representation
    design_name = serializers.CharField(source='design.name', read_only=True)

    class Meta:
        model = CDR
        fields = ['id', 'design', 'design_name', 'generated_by', 'specifications', 'approval_status', 'generated_at']

    # Optional: To include a user-friendly display for the approval status
    def validate_approval_status(self, value):
        if value not in ApprovalStatus.__members__:
            raise serializers.ValidationError(f"{value} is not a valid approval status.")
        return value
