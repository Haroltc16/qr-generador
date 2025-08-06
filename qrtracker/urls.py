from django.contrib import admin
from django.urls import path
from qrs import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.crear_qr, name='crear_qr'),
    path('lista/', views.listar_qrs, name='listar_qrs'),
    path('v/<int:qr_id>/', views.ver_qr, name='ver_qr'),
    
    path('descargar/imagen/<int:qr_id>/', views.descargar_qr_imagen, name='descargar_qr_imagen'),
    path('descargar/pdf/<int:qr_id>/', views.descargar_qr_pdf, name='descargar_qr_pdf'),
    path('detalle/<int:qr_id>/', views.detalle_qr, name='detalle_qr'),
    path('delete_qr/<int:pk>/', views.delete_qr_code, name='delete_qr_code'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

