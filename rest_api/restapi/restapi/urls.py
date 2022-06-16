from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('android_rest.urls')),
    path('mart/',include('martApp.urls'))
]
