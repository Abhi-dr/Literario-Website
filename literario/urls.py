from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('home.urls')),
    
    path('accounts/', include('accounts.urls')),
    path('council/', include('council.urls')),
    path('events/', include('events.urls')),
    
    path("registerMe", views.registerMe, name="registerMe")
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "literario.views.page_not_found_view"

