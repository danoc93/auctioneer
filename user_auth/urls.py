from django.conf.urls import url
from user_auth.views.RegisterUserView import RegisterUserView

urlpatterns = [
    url(r'^register$', RegisterUserView.as_view()),
]
