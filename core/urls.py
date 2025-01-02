from django.urls import path
from .views import (
    UserView,
    DesignView,
    CDRView,
    TokenObtainPairViewCustom,
    GenerateSVGView,
    CDRReportView,
    BoxDesignView,
    LoginView,
    GenerateBoxLayoutView,
)

urlpatterns = [
    # Authentication
    path('token/', TokenObtainPairViewCustom.as_view(), name='token_obtain_pair'),
    
    # User Management
    path('users/', UserView.as_view(), name='user_list_create'),
    
    # Design Management
    path('designs/', DesignView.as_view(), name='design_list_create'),
    
    # CDR Management
    path('cdrs/', CDRView.as_view(), name='cdr_list_create'),
    
    # SVG Generation
    path('generate_svg/', GenerateSVGView.as_view(), name='generate_svg'),
    
    # CDR Report
    path('cdr_report/<int:design_id>/', CDRReportView.as_view(), name='cdr_report'),
    
    # Box Design Management
    path('box_designs/', BoxDesignView.as_view(), name='box_design_list_create'),
    
    # User Login
    path('login/', LoginView.as_view(), name='login'),
    
    # Box Layout Generation
    path('generate_box_layout/', GenerateBoxLayoutView.as_view(), name='generate_box_layout'),
]
    