from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user/', views.UserInfoView.as_view(), name='user'),
    path('subscription/status', views.UserSubscriptionStatusView.as_view(), name='sub_status'),
    path('subscription/toggle', views.UserSubscriptionToggleView.as_view(), name='sub_toggle'),

] 