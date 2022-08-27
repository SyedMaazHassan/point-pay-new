"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404

handler404 = 'authentication.views.error_404_handler'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("landing.urls")),
    path("dashboard/authentication/", include("authentication.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("dashboard/vouchers/", include("vouchers.urls")),
    path("dashboard/students/", include("students.urls")),
    path("dashboard/drivers/", include("drivers.urls")),
    path("dashboard/shuttles/", include("shuttles.urls")),
    path("dashboard/map/", include("map.urls")),
    path("api/", include("api.urls")),
    path("", include("payment.urls")),
]

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)


admin.site.site_header = "Point Pay"
admin.site.site_title = "Point Pay Superadmin"
admin.site.index_title = "Welcome to superadmin portal"