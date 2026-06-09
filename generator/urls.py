from django.urls import path
from . import views

urlpatterns = [
    # e.g., /
    path('', views.home_view, name='home'),
    
    # e.g., /signup/
    path('signup/', views.signup_view, name='signup'),
    
    # e.g., /login/
    path('login/', views.login_view, name='login'),
    
    # e.g., /logout/
    path('logout/', views.logout_view, name='logout'),
    
    # e.g., /generate/90s_anime/
    # This path takes the 'style_id' as a parameter
    path('generate/<str:style_id>/', views.generate_page_view, name='generate_page'),
    
    # e.g., /create-gif/
    path('create-gif/', views.create_gif_view, name='create_gif'),
]