from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from teacherview import views as teach_view
import hashlib

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url="login/")),
    path(hashlib.sha256("students/".encode('utf-8')).hexdigest(),include('studentview.urls')),
    path(hashlib.sha256("teachers/".encode('utf-8')).hexdigest(),include('teacherview.urls')),
    path('login/', teach_view.login_auth, name="login"),
    path('logout/', teach_view.logout_auth, name="logout"),
    path('forgot/', teach_view.forgot_password, name="forgot-password"),
    path("{}<str:email>".format(hashlib.sha256("reset/".encode('utf-8')).hexdigest()), teach_view.reset_password, name="reset-password")
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)