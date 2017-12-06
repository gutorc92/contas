from django.conf.urls import url
from .views import StatementView, DashBoard
from .views import create_statement_type 
from .views import CategoryCreate, CategoryUpdate, CategoryDelete

urlpatterns = [
    url(r'^dashboard/$',DashBoard.as_view(),name='dashboard'),
    url(r'^category/add/$',CategoryCreate.as_view(),name='category'),
    url(r'^category/(?P<pk>[0-9]+)/$',CategoryUpdate.as_view(),name='category-update'),
    url(r'^category/(?P<pk>[0-9]+)/delete/$',CategoryDelete.as_view(),name='category-delete'),
    url(r'^statement/create/(?P<id_type>\d+)/$',StatementView.as_view(),name='statement'),
    url(r'^statement/update/(?P<pk>\d+)/$',StatementView.as_view(),name='statement-update'),
    url(r'^statement/delete/(?P<pk>\d+)/$',StatementView.as_view(),name='statement-delete'),
    url(r'^statement_type/create/$',create_statement_type,name='statement_type'),

]
