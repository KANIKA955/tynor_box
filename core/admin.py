from django.contrib import admin
from .models import User, Design, CDR,BoxDesign

# Register User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('id',)

# Register Design model
@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'user__username')
    ordering = ('id',)

# Register CDR model
@admin.register(CDR)
class CDRAdmin(admin.ModelAdmin):
    list_display = ('id', 'design', 'generated_by', 'approval_status', 'generated_at')
    list_filter = ('approval_status', 'generated_at')
    search_fields = ('design__name', 'generated_by__username')
    ordering = ('id',)
    
@admin.register(BoxDesign)
class BoxDesignAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'width', 'height', 'depth', 'material', 'text', 'created_at']
    list_filter = ('material', 'created_at')
    search_fields = ['material', 'text']
    ordering = ('id',)
