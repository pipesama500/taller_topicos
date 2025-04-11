def rol_usuario(request):
    if request.user.is_authenticated:
        return {'rol_usuario': request.user.id_rol.nombre}  # Suponiendo que el campo 'id_rol.nombre' te da el nombre del rol
    return {'rol_usuario': None}
