from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('wb.urls')),

    path('admin/', admin.site.urls),
]
