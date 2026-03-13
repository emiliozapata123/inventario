from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404
import threading
from django.core.mail import send_mail
import secrets
import string

def generarPassword(len=10):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    password = ""
    for i in range(len):
        password+=secrets.choice(caracteres)
    return password

def enviarCorreo(nombre,correo,password):
    asunto = "Acceso al Sistema de Gestión de Inventario"
    mensaje = (
        f"Estimado/a {nombre},\n\n"
        "Su cuenta ha sido creada exitosamente en el Sistema de Gestión de Inventario.\n\n"
        "Credenciales de acceso:\n"
        f"Usuario: {correo}\n"
        f"Contraseña temporal: {password}\n\n"
        "Por motivos de seguridad, le recomendamos cambiar su contraseña "
        "después de iniciar sesión por primera vez.\n\n"
        "Si tiene problemas para acceder al sistema, comuníquese con el administrador.\n\n"
        "Saludos cordiales,\n"
        "Equipo de soporte\n"
        "Sistema de Gestión de Inventario"
    )

    send_mail(
        asunto,
        mensaje,
        "no-reply@otecprocapacita.com",
        [correo],
        fail_silently=False,
    )
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id","correo","nombre"]
        
class ProfileWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id","correo","nombre"]
        
    def create(self, validated_data):
        request = self.context.get("request")
        password = generarPassword()
        nombre = request.data.get("nombre")
        correo = request.data.get("correo")
        
        username = correo.split("@")[0]
        user = User.objects.create_user(
            username=username,
            password=password
        )
        
        Profile.objects.create(
            user=user,
            nombre=nombre,
            correo=correo
        )
        threading.Thread(
            target=enviarCorreo,
            args=(nombre,
            correo,
            password,
            ),
            daemon=True
        ).start()
        return user
        
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ""
        
#     def create(self, validated_data):
#         request = self.context.data.get("request")
#         password = generarPassword()
#         nombre = request.data.get("nombre")
#         correo = request.data.get("correo")
#         rolID = request.data.get("rol")
        
#         username = correo.split("@")[0]
#         user = User.objects.create_user(
#             username=username,
#             password=password
#         )
#         rol = Rol.objects.get(pk=rolID)
#         Profile.objects.create(
#             user=user,
#             rol=rol,
#             nombre=nombre,
#             correo=correo
#         )
#         threading.Thread(
#             target=enviarCorreo,
#             args=(nombre,
#             correo,
#             password,
#             ),
#             daemon=True
#         ).start()
#         return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # correo = attrs.get("username")
        # password = attrs.get("password")
        
        # user = get_object_or_404(User,correo=correo)
        # if not user.check_password(password):
        #     raise serializers.ValidationError("Error, no se encontro usuario")
        
        # data = super().validate({"username":user.username,"password":password})
        # serializer = UserSerializer(user)
        # data["user"] = serializer.data
        # return data
    
        identificador = attrs.get("username")
        password = attrs.get("password")
        
        user = None
        
        if "@" in identificador:
            profile:Profile = Profile.objects.filter(correo=identificador).first()
            user = profile.user
            
        else:
            try:
                profile:Profile = Profile.objects.filter(rut=identificador).first()
                user = profile.user
            except:
                raise serializers.ValidationError("Usuario no encontrado")
            
        if not user:
            raise serializers.ValidationError("usuario no encontrado")
        
        
        data = super().validate({"username":user.username,"password":password})
        data["user"] = {
            "nombre":profile.nombre,
            "correo":profile.correo
        }
        return data
        