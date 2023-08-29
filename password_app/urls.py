from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('user-login/',views.Login.as_view(),name='user-login'),
    path('user-signup/',views.Signup.as_view(),name='user-signup'),
    path('user-passwords/',views.UserPasswordView.as_view(),name='user-passwords'),
    path('user-password-detail/',views.UsersListView.as_view(),name='user-password-detail'),
    path('users-list/',views.UsersListView.as_view(),name='users-list'),
    path('password-share-detail/',views.PasswordShareView.as_view(),name='password-share-detail'),
    path('shared-password-detail/',views.SharedPasswordView.as_view(),name='shared-password-detail'),
    path('edit-password-reqs/',views.EditPasswordReqsView.as_view(),name='edit-password-reqs'),
    path('password-edit-reqs/',views.PasswordEditReqsView.as_view(),name='password-edit-reqs'),
    path('organisations/',views.OrganisationView.as_view(),name='organisations'),
    path('guest-organisations/',views.GuestOrganisationView.as_view(),name='guest-organisations'),
]