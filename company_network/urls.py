from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("networkapp.urls")),  # 📌 앱의 URL을 포함
]
