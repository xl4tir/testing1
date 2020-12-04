from . import views
from django.urls import path

app_name = "testing"

urlpatterns = [
    path('', views.index, name = 'home'),
    path('test/', views.test, name = 'test'),
    path('test/<int:testcode>/', views.about_test, name = 'about_test'),
    path('test/create/', views.create, name = 'create'),
    path('test/create/create_page', views.create_page, name = 'create_page'),
    path('test/builder/<int:code>/', views.builder, name = 'builder'),
    path('test/builder/<int:code>/add_ques', views.add_ques, name = 'add_ques'),
    path('test/builder/<int:code>/delete_ques/<int:ques_num>', views.delete_ques, name = 'delete_ques'),
    path('test/builder/<int:code>/edit_ques/<int:ques_num>', views.edit_ques, name = 'edit_ques'),
    path('test/builder/<int:code>/editing_ques/<int:ques_num>', views.editing_ques, name = 'editing_ques'),
    path('test/builder/<int:code>/add_ques/adding_ques', views.adding_ques, name = 'adding_ques'),
    path('test/testing/<token>/', views.testing, name = 'testing'),
    path('test/testing/<token>/processing', views.processing, name = 'processing'),
    path('test/complete/<token>', views.complete, name = 'complete'),
    path('login/', views.MyprojectLoginView.as_view(), name = 'login'),
    path('register/', views.RegisterUserView.as_view(), name = 'register'),
    path('profile/', views.profile, name = 'profile'),
    path('detele_test/<int:code>/', views.detele_test, name = 'detele_test'),
    path('logout/', views.MyProjectLogout.as_view(), name = 'logout'),

]
