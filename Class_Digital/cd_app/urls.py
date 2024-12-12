from django.urls import path
from cd_app import views 

app_name = 'cd_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.edit_profile, name='profile'),
    path('forum/', views.forum_view, name='forum'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('task/', views.task_view, name='task'),
    path('presence/', views.presence_view, name='presence'),
    path('recap/', views.recap_view, name='recap'),
    path('list/', views.list_view, name='list'),
    path('logout/', views.logout_view, name='logout'),
]
