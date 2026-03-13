from django.urls import path
from .views import CustomTokenObtainPairView,ProfileView,UserView,CurrentUserView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/list/',ProfileView.as_view()),
    path('profile/form/',ProfileView.as_view()),
    path('user/update/',UserView.as_view()),
    path('current-user/',CurrentUserView.as_view()),    
    path('profile/<int:id>/delete/',ProfileView.as_view()),    

]