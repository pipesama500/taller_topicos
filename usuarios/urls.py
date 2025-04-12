from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (
    UsuarioListView,
    UsuarioCreateView,
    UsuarioUpdateView,
    UsuarioDeleteView,)

urlpatterns = [
    # Autenticación
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboard general
    path('dashboard/', views.dashboard, name='dashboard'),

    # Sección: Portero
    path('portero/dashboard/', views.portero_dashboard, name='portero_dashboard'),
    path('portero/torres/', views.portero_dashboard, name='portero_torres'),  # Ejemplo: se reusa la vista
    path('portero/torres/<int:torre_id>/pisos/', views.portero_pisos, name='portero_pisos'),
    path('portero/pisos/<int:piso_id>/apartamentos/', views.portero_apartamentos, name='portero_apartamentos'),
    path('portero/apartamentos/<int:apartamento_id>/', views.portero_detalle_apartamento, name='portero_detalle_apartamento'),

    # Pendientes e historial (agrupado por rol)
    path('portero/pendientes/', views.pendientes_portero, name='portero_pendientes'),
    path('portero/historial/', views.historial_portero, name='portero_historial'),
    path('residente/pendientes/', views.pendientes_residente, name='residente_pendientes'),
    path('residente/historial/', views.historial_residente, name='residente_historial'),

    # Sección: Residente
    path('residente/dashboard/', views.residente_dashboard, name='residente_dashboard'),
    path('residente/notificaciones/', views.notificaciones_residente, name='notificaciones_residente'),

    # Usuarios
    #path('usuarios/', views.lista_usuarios, name='usuarios_list'),   # GET: lista usuarios
    #path('usuarios/create/', views.crear_usuario, name='usuarios_create'), 
    #path('usuarios/<int:usuario_id>/edit/', views.editar_usuario, name='usuarios_edit'),
    #path('usuarios/<int:usuario_id>/delete/', views.eliminar_usuario, name='usuarios_delete'),
    path('', UsuarioListView.as_view(), name='usuarios_list'),
    path('create/', UsuarioCreateView.as_view(), name='usuarios_create'),
    path('<int:pk>/edit/', UsuarioUpdateView.as_view(), name='usuarios_edit'),
    path('<int:pk>/delete/', UsuarioDeleteView.as_view(), name='usuarios_delete'),

    # Anuncios
    path('anuncios/', views.lista_anuncios, name='anuncios_list'),
    path('anuncios/create/', views.crear_anuncio, name='anuncios_create'),

    # Visitas (subsección para residente)
    path('residente/visitas/new/', views.nueva_visita, name='residente_visita_new'),
    path('residente/visitas/<int:visita_id>/confirmacion_frecuente/', 
         views.confirmacion_visita_frecuente, name='residente_visita_confirmacion'),

    # Domicilios y Paquetes (subsección para residente)
    path('residente/domicilios/new/', views.nuevo_domicilio, name='residente_domicilio_new'),
    path('residente/paquetes/new/', views.nuevo_paquete, name='residente_paquete_new'),

    # Creación “inesperada” (subsección para portero)
    path('portero/visitas/unexpected/new/', views.crear_visita_inesperada, name='portero_visita_unexpected'),
    path('portero/domicilios/unexpected/new/', views.crear_domicilio_inesperado, name='portero_domicilio_unexpected'),
    path('portero/paquetes/unexpected/new/', views.crear_paquete_inesperado, name='portero_paquete_unexpected'),

    # Confirmar pendientes (ejemplo: /confirmar/5/domicilio/)
    path('confirmar/<int:pendiente_id>/<str:tipo>/', views.confirmar_pendiente, name='confirmar_pendiente'),

    # Verificación QR
    path('portero/apartamentos/<int:apartamento_id>/verificar_qr/', views.verificar_qr, name='verificar_qr'),

    # Perfil
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
