from django.urls import path
from core.security.views.user_access.views import *

urlpatterns = [
    path('user/access/', UserAccessListView.as_view(), name='user_access_list'),
    path('user/access/add/', UserAccessDeleteView.as_view(), name='user_access_create'),
]
