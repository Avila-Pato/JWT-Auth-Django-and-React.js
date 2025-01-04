from django.shortcuts import render  # Importación estándar de Django para manejar vistas (no se utiliza aquí).
from rest_framework.generics import GenericAPIView, RetrieveAPIView  # Clases base para crear vistas genéricas en Django REST Framework.
from rest_framework.permissions import AllowAny, IsAuthenticated  # Permisos para manejar acceso a las vistas.
from .serializers import *  # Importación de todos los serializadores definidos en el archivo serializers.py.
from .serializers import CustomUserSerializer  # Importación del serializador CustomUserSerializer.
from rest_framework_simplejwt.tokens import RefreshToken  # Módulo para trabajar con tokens JWT.
from rest_framework.response import Response  # Clase para generar respuestas HTTP.
from rest_framework import status  # Constantes de códigos de estado HTTP.

# Vista que permite a los usuarios registrarse mediante la API.
class UserRegistrationAPIViews(GenericAPIView):
    permission_classes = (AllowAny,)  # Permite acceso a cualquier usuario, autenticado o no.
    serializer_class = UserRegistrationSerializer  # Asigna el serializador para manejar los datos.

    def post(self, request, *args, **kwargs):  # Método que maneja solicitudes POST.
        serializers = self.get_serializer(data=request.data)  # Crea una instancia del serializador con los datos enviados.
        serializers.is_valid(raise_exception=True)  # Valida los datos, lanza un error si no son válidos.
        user = serializers.save()  # Guarda el usuario en la base de datos.
        token = RefreshToken.for_user(user)  # Genera un token JWT para el usuario recién creado.
        data = serializers.data  # Obtiene los datos serializados del usuario.
        data["tokens"] = {  # Añade los tokens de acceso y actualización a la respuesta.
            "refresh": str(token),
            "access": str(token.access_token),
        }
        return Response(data, status=status.HTTP_201_CREATED)  # Devuelve una respuesta con los datos del usuario y un código 201 (creado).

# Vista que permite iniciar sesión en la API.
class UserLogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)  # Solo permite acceso a usuarios autenticados.
    serializer_class = UserLoginSerializer  # Utiliza un serializador para validar los datos de inicio de sesión.

    def post(self, request, *args, **kwargs):  # Método que maneja solicitudes POST para login.
        serializers = self.get_serializer(data=request.data)  # Valida los datos enviados en la solicitud.
        serializers.is_valid(raise_exception=True)  # Lanza un error si los datos son inválidos.
        user = serializers.validated_data  # Obtiene los datos validados.
        serializers = CustomSerializer(user)  # Serializa al usuario autenticado.
        token = RefreshToken.for_user(user)  # Genera un token JWT para el usuario.
        data = serializers.data  # Obtiene los datos serializados.
        data["tokens"] = {  # Añade los tokens de acceso y actualización.
            "refresh": str(token),
            "access": str(token.access_token),
        }
        return Response(data, status=status.HTTP_201_CREATED)  # Respuesta con los datos del usuario y el código 201.

# Vista para cerrar sesión, invalidando el token de actualización.
class UserLogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)  # Solo permite acceso a usuarios autenticados.

    def post(self, request, *args, **kwargs):  # Maneja solicitudes POST para logout.
        try:
            refresh_token = request.data["refresh"]  # Obtiene el token de actualización de los datos enviados.
            token = RefreshToken(refresh_token)  # Crea una instancia del token.
            token.blacklist()  # Añade el token a la lista negra para invalidarlo.
            return Response(status=status.HTTP_205_RESET_CONTENT)  # Respuesta indicando que el contenido se ha reseteado.
        except Exception as e:  # Captura excepciones si el proceso falla.
            return Response(status=status.HTTP_400_BAD_REQUEST)  # Respuesta con error 400 en caso de falla.

# Vista para obtener información del usuario autenticado.
class UserInfoAOIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)  # Solo permite acceso a usuarios autenticados.
    serializer_class = CustomUserSerializer  # Serializador para estructurar los datos del usuario.

    def get_object(self):  # Método para obtener el objeto que representa al usuario.
        return self.request.user  # Devuelve el usuario autenticado.
