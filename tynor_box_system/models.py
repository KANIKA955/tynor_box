from django.db import models
from django.contrib.auth import get_user_model  # Use get_user_model() to get the CustomUser model
from enum import Enum

# Enum for design approval status
class ApprovalStatus(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    @classmethod
    def choices(cls):
        # Returns a list of tuples with (value, human-readable name)
        return [(tag.value, tag.name.capitalize()) for tag in cls]

# Design model for storing design information, including uploaded files
class Design(models.Model):
    file = models.FileField(upload_to='designs/', null=True, blank=True)  # This field stores the uploaded design files
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Link to the user who created the design
    name = models.CharField(max_length=255)  # Name of the design
    version = models.CharField(max_length=50)  # Version of the design
    dimensions = models.JSONField()  # Dimensions of the design in JSON format
    material_specs = models.JSONField()  # Material specifications in JSON format
    approval_status = models.CharField(
        max_length=20, 
        choices=ApprovalStatus.choices(), 
        default=ApprovalStatus.PENDING.value
    )  # Status of design approval
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the design was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the design was last updated

    def __str__(self):
        return f"Design: {self.name} (Version: {self.version}), Status: {self.get_approval_status_display()}"  # Enhanced string representation

# CDR (Customer Design Report) model for storing design approval and report information
class CDR(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE)  # Link to the design this report is related to
    generated_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # User who generated the report
    specifications = models.JSONField()  # JSON format for design specifications
    approval_status = models.CharField(
        max_length=20, 
        choices=ApprovalStatus.choices(),
        default=ApprovalStatus.PENDING.value
    )  # Approval status of the report
    generated_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the CDR was generated

    def __str__(self):
        return f"CDR for {self.design.name} (Version {self.design.version}) by {self.generated_by.username}, Status: {self.get_approval_status_display()}"  # Enhanced string representation
