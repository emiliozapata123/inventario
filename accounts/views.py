from django.shortcuts import render
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Profile,User
from .serializers import ProfileSerializer, ProfileWriteSerializer
from rest_framework.views import APIView,Response,status
from rest_framework.permissions import IsAuthenticated

# Create your views here.

def validarPassword(password):
    numero = False
    mayuscula = False
    minuscula = False
    
    for letra in password:
        if "a" < letra < "z":
            minuscula = True
        if "A" < letra < "Z":
            mayuscula = True
        if "0" < letra < "9":
            numero = True
            
    if not numero or not mayuscula or not minuscula:
        return False
    return True


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        usuarios = Profile.objects.all()
        serializer = ProfileSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProfileWriteSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request,id):
        user = request.user
        try:
            profile = Profile.objects.get(pk=id)
            
            if profile.user == user:
                return Response({"error":"no puedes eliminar tu propio usuario"}, status=status.HTTP_400_BAD_REQUEST)
            
            if User.objects.count() <= 1:
                return Response({"error":"debe existir al menos un usuario en el sistema"})
            
            profile.user.delete()
        
        except Profile.DoesNotExist:
            return Response({"error":"usuario no encontrado"},status=status.HTTP_404_NOT_FOUND)
            
    
class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        password = request.data.get("password")
        
        validar = validarPassword(password)
        if not validar:
            return Response({"error","contraseña no valido"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        
        user.set_password(password)
        user.save()
        
        return Response(status=status.HTTP_200_OK)
    
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
