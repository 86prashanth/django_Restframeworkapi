from django.contrib import admin 
from django.urls import path,include
from rest_framework.routers import DefaultRouter
# from watchlist_app.api.views import MovieListAV,MovieDetailAV
from watchlist_app.api.views import UserReview, ReviewList,ReviewDetail,Watchlist,WatchListAV,WatchDetailAV,StreamplatFormAV,StreamDetailAV,ReviewCreate,StreamPlatFormVS,StreamPlatFormSv
# from watchlist_app.api.views import movie_list,movie_details

router=DefaultRouter()
# router.register('stream/',StreamPlatFormVS,basename='streamplatform'),
router.register('streamvs',StreamPlatFormSv,basename='streamplatform'),
urlpatterns=[
    
    path('list/',WatchListAV.as_view(),name='movie_list'),
    path('list2/',Watchlist.as_view(),name='watch_list'),
    path('<int:pk>',WatchDetailAV.as_view(),name='movie_details'),
    path('stream/',StreamplatFormAV.as_view(),name='stream-list'),
    path('stream/<int:pk>/',StreamDetailAV.as_view(),name='streamplatform-detail'),
    path('stream/<int:pk>/review/',StreamDetailAV.as_view(),name='streamplatform-detail'),
    path('',include(router.urls)),
    path('review/',UserReview.as_view(),name='user_review_detail'),
    path('review/<int:pk>/',ReviewList.as_view(),name='review_list'),
    path('<int:pk>/review/',ReviewCreate.as_view(),name='reviewcreate'),
    path('review/detail/<int:pk>/',ReviewDetail.as_view(),name='reviewdetial'),
    # path('review/<int:pk>/',ReviewList.as_view(),name='review_list'),
    # path('review/<int:pk>/',ReviewDetail.as_view(),name='review_detail'),
    # path('list/',MovieListAV.as_view(),name='movie_list'),
    # path('<int:pk>/',MovieDetailAV.as_view(),name='movie_details'),
    # path('list/',movie_list,name='movie_list'),
    # path('<int:pk>',movie_details,name='movie_details'),
]
    