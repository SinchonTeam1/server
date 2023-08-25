from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include("users.urls")),
    path('api/study/', include('studies.urls')),
    path('api/details/', include('details.urls')),
    path('api/mypages/', include('mypages.urls')),

]