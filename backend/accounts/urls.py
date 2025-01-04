from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView, UserInfoAPIView
from rest_framework_simplejwt.views import TokenRefreshView

# Definición de las rutas de la aplicación.
urlpatterns = [
    # Ruta para registrar nuevos usuarios.
    path(
        "register/",  # URL endpoint para el registro de usuarios.
        UserRegistrationAPIView.as_view(),  # Llama a la vista `UserRegistrationAPIView`.
        name="register-user"  # Nombre único para referenciar esta ruta en el proyecto.
    ),

    # Ruta para iniciar sesión (login) de usuarios.
    path(
        "login/",  # URL endpoint para login.
        UserLoginAPIView.as_view(),  # Llama a la vista `UserLoginAPIView`.
        name="login-user"  # Nombre único para esta ruta.
    ),

    # Ruta para cerrar sesión (logout) de usuarios.
    path(
        "logout/",  # URL endpoint para logout.
        UserLogoutAPIView.as_view(),  # Llama a la vista `UserLogoutAPIView`.
        name="logout-user"  # Nombre único para esta ruta.
    ),

    # Ruta para refrescar el token JWT.
    path(
        "token/refresh/",  # URL endpoint para refrescar tokens.
        TokenRefreshView.as_view(),  # Utiliza la vista `TokenRefreshView` de DRF Simple JWT.
        name="token-refresh"  # Nombre único para esta ruta.
    ),

    # Ruta para obtener información del usuario autenticado.
    path(
        "user/",  # URL endpoint para consultar información del usuario.
        UserInfoAPIView.as_view(),  # Llama a la vista `UserInfoAPIView`.
        name="user-info"  # Nombre único para esta ruta.
    ),
]