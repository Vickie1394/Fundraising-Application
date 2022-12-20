from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.urls import path,reverse,reverse_lazy, re_path

app_name = "fundraiser"

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('fundraising_event/<str:code>', views.fundraising_event, name = "fundraising_event"),
    path('create_fundraising_event', views.create_fundraising_event, name = "create_fundraising_event"),
    path('join_fundraising_event/<str:code>', views.join_fundraising_event, name = "join_fundraising_event"),
    path('donate', views.donate, name="donate"),
    path('register', views.register, name="register"),
    path('login_user', views.login_user, name="login_user"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('profile', views.profile, name="profile"),
    path('contact_us', views.contact_us, name="contact_us"),
    path('about_us', views.about_us, name="about_us"),
    path('how_it_works', views.how_it_works, name="how_it_works"),
    path('our_services', views.our_services, name="our_services"),
    path('activation_sent/', views.activation_sent_view,name='activation_sent'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name = 'activate'),
    path('password_reset/', auth_views.PasswordResetView.as_view(email_template_name = 'fundraiser/password_reset_email.html',
                                                                 success_url = reverse_lazy('fundraiser:password_reset_done')), name='password_reset'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name = 'fundraiser/password_reset_done.html'), name='password_reset_done'),

    path('password_reset_<uidb64>_<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'fundraiser/password_reset_confirm.html',
                                                                                         success_url = reverse_lazy('fundraiser:password_reset_complete')), name='password_reset_confirm'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'fundraiser/password_reset_complete.html'), name='password_reset_complete'),
]
