from django.conf.urls import url

from user_auth.views.LoginUserView import LoginUserView
from user_auth.views.RegisterUserView import RegisterUserView
from user_auth.views.RevokeTokenView import RevokeTokenView
from user_auth.views.RefreshTokenView import RefreshTokenView

urlpatterns = [
    url(r'^register$', RegisterUserView.as_view()),
    url(r'^login$', LoginUserView.as_view()),
    url(r'^revoke$', RevokeTokenView.as_view()),
    url(r'^refresh$', RefreshTokenView.as_view())
]
