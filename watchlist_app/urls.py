from django.urls import path 
from watchlist_app.views import *


urlpatterns=[ 
    path('movie_list/',movie_list,name='movielist'),
    path('movie/<int:pk>/',movie_detail,name='moviedetail'),
]

                      