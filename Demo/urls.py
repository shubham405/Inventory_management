from django.urls import path,include
from . import views
urlpatterns = [

    path('', views.index, name='index'),
    path('tables', views.tables, name = 'tables'),
    path('predict', views.predict, name = 'predict'),

]