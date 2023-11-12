from django.urls import path
from notes import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('reg/', views.reg_page, name='registration'),
    path('login/',  views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('notes/', views.show_notes_page, name='notes'),
    path('add_note/', views.add_note_page, name='add_note'),
]