from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from teacherview import views as teach_view
import hashlib
from django.conf.urls import handler404, handler500, handler403, handler400
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url="login/")),
    path('students/',include('studentview.urls')),
    path('teachers/',include('teacherview.urls')),
    path('login/', teach_view.login_auth, name="login"),
    path('logout/', teach_view.logout_auth, name="logout"),
    path('forgot/', teach_view.forgot_password, name="forgot-password"),
    path('security-questions/<str:email>', teach_view.security_questions, name="security-questions"),
    path('reset-password/<str:email>/<str:code>', teach_view.reset_password, name="reset_password"),
]

handler400 = 'studentview.views.error_400'
handler403 = 'studentview.views.error_403'
handler404 = 'studentview.views.error_404'
handler500 = 'studentview.views.error_500'

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)