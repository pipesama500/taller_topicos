from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    
    path('', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('portero/', views.portero_dashboard, name='portero_dashboard'),
    path('residente/dashboard/', views.residente_dashboard, name='residente_dashboard'),
    path('administrador/dashboard', views.administrador_dashboard, name='administrador_dashboard'),

    path('crear_anuncio/', views.crear_anuncio, name='crear_anuncio'),
    path('anuncios/', views.lista_anuncios, name='lista_anuncios'),

    # Nuevas rutas para las vistas que cargan los templates de nueva visita, nuevo domicilio y nuevo paquete
    path('residente/nueva-visita/', views.nueva_visita, name='nueva_visita'),
    path('residente/nuevo-domicilio/', views.nuevo_domicilio, name='nuevo_domicilio'),
    path('residente/nuevo-paquete/', views.nuevo_paquete, name='nuevo_paquete'),

    path('portero/torres/', views.portero_dashboard, name='portero_dashboard'),
    path('portero/torre/<int:torre_id>/pisos/', views.portero_pisos, name='portero_pisos'),
    path('portero/piso/<int:piso_id>/apartamentos/', views.portero_apartamentos, name='portero_apartamentos'),
    path('portero/apartamento/<int:apartamento_id>/', views.portero_detalle_apartamento, name='portero_detalle_apartamento'),


    path('portero/pendientes/', views.pendientes_portero, name='pendientes_portero'),
    path('residente/pendientes/', views.pendientes_residente, name='pendientes_residente'),
    path('residente/historial/', views.historial_residente, name='historial_residente'),
    path('portero/historial/', views.historial_portero, name='historial_portero'),
    path('portero/verificar_qr/<int:apartamento_id>/', views.verificar_qr, name='verificar_qr'),
    path('residente/confirmacion_visita_frecuente/<int:visita_id>/', views.confirmacion_visita_frecuente, name='confirmacion_visita_frecuente'),

    # Nueva ruta para las notificaciones del residente
    path('residente/notificaciones/', views.notificaciones_residente, name='notificaciones_residente'),


    path('portero/crear-visita-inesperada/', views.crear_visita_inesperada, name='crear_visita_inesperada'),
    path('portero/crear-domicilio-inesperado/', views.crear_domicilio_inesperado, name='crear_domicilio_inesperado'),
    path('portero/crear-paquete-inesperado/', views.crear_paquete_inesperado, name='crear_paquete_inesperado'),
    path('confirmar/<int:pendiente_id>/<str:tipo>/', views.confirmar_pendiente, name='confirmar_pendiente'),

    path('perfil/', views.perfil_usuario, name='perfil_usuario'),

     path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
