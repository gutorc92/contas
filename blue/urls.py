from django.conf.urls import url
from blue import views

urlpatterns = [
    url(r'^category/create/$',views.create_category,name='category'),
    url(r'^statement/create/$',views.create_statement,name='statement'),
    url(r'^statement_type/create/$',views.create_statement_type,name='statement_type'),

]
