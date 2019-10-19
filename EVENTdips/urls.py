from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
import teacherview.views as teach_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='teachers/', permanent=False)),
    path('students/',include('studentview.urls')),
    path('teachers/',include('teacherview.urls')),
    path('login/', teach_view.login_auth, name="login"),
    path('logout/', teach_view.logout_auth, name="logout")
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)