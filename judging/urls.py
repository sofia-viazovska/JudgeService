from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('teams/', views.team_list, name='team_list'),
    path('judge/<int:team_id>/', views.judge_team, name='judge_team'),
    path('results/', views.results, name='results'),
    path('admin-scores/', views.admin_detailed_scores, name='admin_detailed_scores'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='judging/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
