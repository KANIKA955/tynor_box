from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    
     # Box Layout HTML
    path('box-layout/', TemplateView.as_view(template_name="box_layout.html"), name='box_layout'),
]
