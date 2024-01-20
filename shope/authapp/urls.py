from django.urls import path
from authapp.views import UserLoginView, UserLogoutView, UserSignUpView, \
    verify_user, UserPassResetView, UserPassChangeView

app_name = 'authapp'

urlpatterns = [
    path('forgot-password/', UserPassResetView.as_view(),
         name='forgot_pass'),
    path('login/', UserLoginView.as_view(),
         name='login'),
    path('set-password/<uidb64>/<token>/', UserPassChangeView.as_view(),
         name='set_pass'),
    path('signup/', UserSignUpView.as_view(),
         name='signup'),
    path('logout/', UserLogoutView.as_view(),
         name='logout'),
    path('verified/<str:email>/<str:key>/', verify_user,
         name='verified'
         ),
]
