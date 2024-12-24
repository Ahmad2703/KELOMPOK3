from django.urls import path
from cd_app import views 
from django.conf import settings
from django.conf.urls.static import static
#from .views import delete_comment

app_name = 'cd_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.edit_profile, name='profile'),
    #path('forum/', views.forum_view, name='forum'),
    path('forum/<int:course_id>/', views.forum_view, name='forum'),
    #path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('calendar/', views.calendar_view, name='calendar'),
    #path('task/', views.task_view, name='task'),
    path('task/<int:course_id>/', views.task_view, name='task'),
    #path('task/<int:course_id>/upload_material/', views.upload_material, name='upload_material'),
    #path('presence/', views.presence_view, name='presence'),
    path('presence/<int:course_id>/', views.presence_view, name='presence'),
    path('recap/<int:course_id>/', views.recap_view, name='recap'),
    path('list/<int:course_id>/', views.list_view, name='list'),
    path('setting/', views.setting_view, name='setting'),
    path('logout/', views.logout_view, name='logout'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)