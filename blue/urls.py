from django.conf.urls import url
from .views import StatementView
from .views import create_category, create_statement_type 

urlpatterns = [
    url(r'^category/create/$',create_category,name='category'),
    url(r'^statement/create/(?P<id_type>\d+)/$',StatementView.as_view(),name='statement'),
    url(r'^statement_type/create/$',create_statement_type,name='statement_type'),

]
