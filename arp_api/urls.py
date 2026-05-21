from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('admin/', admin.site.urls),

    path('api/', include('api_workflow.urls')),

    path('auth/', include('accounts.urls')),

]
