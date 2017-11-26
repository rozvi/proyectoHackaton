from django.conf.urls import url,include
from django.contrib import admin
from pruebaHackaton import views
from rest_framework.urlpatterns import format_suffix_patterns




urlpatterns = [
  	
    url(r'^persona/$',views.PersonList.as_view()),#name='index'),
    
    url(r'^objeto/$',views.person_list,name='listaPersona'),
    #url(r'^/persona', ListCreateAPIView.as_view(queryset=Person.objects.all(), serializer_class=PersonSerializer), name='user-list')
    url(r'^prueba/$',views.index,name='index'),
    url(r'^login/$',views.usuarioValidacion, name='usuario'),
    
]

urlpatterns=format_suffix_patterns(urlpatterns)