from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

# Custom User Model
class User(AbstractUser):
    """
    Custom user model with role-based access control.
    """
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Designer', 'Designer'),
        ('Reviewer', 'Reviewer'),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Designer')

    def __str__(self):
        return self.username


# Core Design Model
class Design(models.Model):
    """
    Model for managing core designs.
    """
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="core_designs"
    )  # Unique related_name for core app
    name = models.CharField(max_length=255)
    version = models.PositiveIntegerField(default=1)  # Only allow positive integers
    dimensions = models.JSONField(default=dict)  # Example: {"width": 10, "height": 20}
    material_specs = models.JSONField(default=dict)  # Example: {"type": "Plastic", "color": "Blue"}
    status = models.CharField(
        max_length=50,
        choices=(('Pending', 'Pending'), ('Approved', 'Approved')),
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (v{self.version})"


# Tynor Box System Design Model
class DesignTynorBox(models.Model):
    """
    Model for managing Tynor Box System designs.
    """
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="tynor_box_designs"
    )
    name = models.CharField(max_length=255)
    version = models.PositiveIntegerField(default=1)
    dimensions = models.JSONField(default=dict)
    material_specs = models.JSONField(default=dict)
    status = models.CharField(
        max_length=50,
        choices=(('Pending', 'Pending'), ('Approved', 'Approved')),
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (v{self.version})"


# CDR Model (CorelDRAW Reports)
class CDR(models.Model):
    """
    Model for managing CorelDRAW reports for designs.
    """
    design = models.ForeignKey(
        Design,
        on_delete=models.CASCADE,
        related_name="cdrs"
    )
    generated_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="generated_cdrs"
    )
    specifications = models.TextField()
    approval_status = models.CharField(
        max_length=50,
        choices=(('Pending', 'Pending'), ('Approved', 'Approved')),
        default='Pending'
    )
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CDR for {self.design.name} by {self.generated_by.username}"


class BoxDesign(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="box_designs")
    width = models.FloatField(help_text="Width of the box in cm.")
    height = models.FloatField(help_text="Height of the box in cm.")
    depth = models.FloatField(help_text="Depth of the box in cm.")
    material = models.CharField(
        max_length=50,
        choices=(('Cardboard', 'Cardboard'), ('Plastic', 'Plastic'), ('Metal', 'Metal')),
        help_text="Material of the box."
    )
    text = models.TextField(help_text="Text or description on the box.")
    logo = models.ImageField(upload_to="logos/", help_text="Logo image for the box design.")
    approval_status = models.CharField(
        max_length=50,
        choices=(('Pending', 'Pending'), ('Approved', 'Approved')),
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Box Design: {self.text} ({self.width}x{self.height}x{self.depth})"
