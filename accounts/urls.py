from django.urls import path
from .views import register, login, dashboard, edit_password, my_courses, logout

urlpatterns = [
    path('register', register, name='register'),
    path('login', login, name='login'),
    path('dashboard', dashboard, name='dashboard'),
    path('edit_password', edit_password, name='edit_password'),
    path('my_courses', my_courses, name='my_courses'),
    path('logout', logout, name='logout')
]
