from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='teachers/', permanent=False)),
    path('students/',include('studentview.urls')),
    path('teachers/',include('teacherview.urls')),
    path('login/', auth_view.LoginView.as_view(template_name="studentview/login.html", extra_context={'title':'Login'}), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name="studentview/logout.html"), name="logout")
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)