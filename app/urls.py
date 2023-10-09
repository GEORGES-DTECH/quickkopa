from django.contrib import admin
from django.urls import path, include
from . import settings
from transactions import views

from django.conf.urls.static import static
admin.site.site_header  =  "Repotrans administration" 
admin.site.site_title  =  "Repotrans admin dashboard"
import debug_toolbar

urlpatterns = [
    path("root/", admin.site.urls, name="manager"),
    path("", include("transactions.urls")),
    path("", include("pwa.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("sms-services/", include("sms_services.urls")),
    path("accounts/", include("accounts.urls")),
    path("select2/", include("django_select2.urls")),
    
    path(".well-known/assetlinks.json/", views.assetlinks, name="assets"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
