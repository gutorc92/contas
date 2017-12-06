from django.conf.urls import include, url

from . import views
from .views import LoginView, MainView, UserRegister, UserListView
from .views import UserDeleteView, UserChangeGroupView
from .views import FamilyView, FamilyAcceptView

urlpatterns = [
    url(r'^family/list', FamilyView.as_view(), name='family-list'),
    url(r'^family/member-invitation', FamilyView.as_view(), name='member-invitation'),
    url(r'^family/accept/(?P<id_invitation>\d+)', FamilyAcceptView.as_view(), name='family-accept'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LoginView.as_view(), name='logout'),
    url(r'^view/', MainView.as_view(), name='logged'),
    url(r'^signin/', UserRegister.as_view(), name='signin'),
    url(r'^all/', UserListView.as_view(), name='list_users'),
    url(r'^delete/(?P<id_user>\d+)/(?P<action>\w+)/', UserDeleteView.as_view(), name='delete_user'),
    url(r'^changegroup/(?P<id_user>\d+)/(?P<group_change_to>\w+)/', UserChangeGroupView.as_view(), name='changegroup_user'),
]
