from django.shortcuts import render
from rest_framework import status,generics,mixins,viewsets 
from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.api.throttling import ReviewCreateThrottle,ReviewListThrottle
from watchlist_app.api.permissions import AdminOrReadOnly,ReviewUserOrReadOnly
from watchlist_app.models import *
from watchlist_app.api.pagination import WatchListPagination,watchLpagination,WatchCpagination
from watchlist_app.api.serializers import WatchListSerializers,StreamPlatFormSerializers,ReviewSerializers

# Create your views here.
# filtering 
class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class=ReviewSerializers
    # permission_classes=[IsAuthenticated]
    # # throttle_classes=[ReviewCreateThrottle,ReviewListThrottle]
    def get_queryset(self):
        # username=self.kwargs['username']
        username=self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username)
    # def get_queryset(self):
    #     queryset = Review.objects.all()
    #     username=self.request.query_params.get('username',None)
    #     if username is not None:
    #         queryset=queryset.filter(purchaser__username=username)
    #     return queryset
    
class ReviewCreate(generics.CreateAPIView):
    # queryset = Review.objects.all()``
    serializer_class=ReviewSerializers
    throttle_classes=[ReviewCreateThrottle]
    def get_queryset(self):
        return Review.objects.all()
    def perform_create(self,serializer):
        pk=self.kwargs.get('pk')
        watchlist=WatchList.objects.get(pk=pk)
        review_user=self.request.user
        review_queryset=Review.objects.filter(watchlist=watchlist, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")
        if watchlist.number_rating==0:
            watchlist.avg_rating=serializer.validated_data['rating']
        else:
            watchlist.avg_rating=(watchlist.avg_rating + serializer.validated_data['rating'])/2
        watchlist.number_rating=watchlist.number_rating+1
        watchlist.save()
        serializer.save(watchlist=watchlist,review_user=review_user)
    
    
# class ReviewList(generics.ListCreateAPIView):
class ReviewList(generics.ListAPIView):
    # queryset=Review.objects.all()
    serializer_class=ReviewSerializers
    # permission_classes=[IsAuthenticatedOrReadOnly]
    permission_classes=[IsAuthenticated]
    throttle_classes=[ReviewListThrottle,AnonRateThrottle]
    filter_backends=[DjangoFilterBackend]
    filterset_fileds=['review_user__username','active']
    
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializers
    # permission_classes=[IsAuthenticated]
    permission_classes=[AdminOrReadOnly]
    # permission_classes=[ReviewUserOrReadOnly]
    throttle_classes=[UserRateThrottle,AnonRateThrottle]
#viewsets and routers 
class StreamPlatFormVS(viewsets.ViewSet):
    def list(self,request):
        queryset=StreamPlatForm.objects.all()
        serializer=StreamPlatFormSerializers(queryset,many=True,context={'request':request})
        return Response(serializer.data)
    
    def retrive(self,request,pk=None):
        queryset=StreamPlatForm.objects.all()
        watchlist=get_object_or_404(queryset,pk=pk)
        serializer=StreamPlatFormSerializers(watchlist)
        return Response(serializer.data)
    
    def create(self,request):
        serializer=StreamPlatFormSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    def delete(self,request,pk):
        movie=StreamPlatForm.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StreamPlatFormSv(viewsets.ModelViewSet):
# class StreamPlatFormSv(viewsets.ReadOnlyModelViewSet):
    queryset=StreamPlatForm.objects.all()
    serializer_class=StreamPlatFormSerializers

# movie_list
# @api_view(['GET','POST'])
# def movie_list(request):
#     if request.method=='GET':
#         movie=Movie.objects.all()
#         serializers=MovieSerializers(movie,many=True)
#         return Response(serializers.data)
    
#     if request.method=='POST':
#         serializer=MovieSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
# @api_view(['GET','PUT','DELETE'])
# def movie_details(request,pk):
#     if request.method=='GET':
#         try:
#             movie=Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error':'Movie Not found'},status=status.HTTP_404_NOT_FOUND)
#         serializer=MovieSerializers(movie)
#         return Response(serializer.data)
    
#     if request.method=='PUT':
#         movie=Movie.objects.get(pk=pk)
#         serializer=MovieSerializers(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
#     if request.method=='DELETE':
#         movie=Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        
# class based views 
# class MovieListAV(APIView):
#     def get(self,request):
#         movies=Movie.objects.all()
#         serializer=MovieSerializers(movies,many=True)
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer=MovieSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
class WatchListAV(APIView):
    def get(self,request):
        movies=WatchList.objects.all()
        serializer=WatchListSerializers(movies,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=WatchListSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class Watchlist(generics.ListAPIView):
    queryset=WatchList.objects.all()
    serializer_class=WatchListSerializers
    # pagination_class=WatchCpagination
    # filter_backends=[DjangoFilterBackend]
    # filter_backends=[filters.SearchFilter]
    # filter_backends=[filters.OrderingFilter]
    # ordering_fields=['avg_rating']
    # filterset_filds=['title','platform__name']
    filterset_filds=['title','platform__name']
    pagination_class=WatchListPagination
    # pagination_class=watchLpagination
    
# class MovieDetailAV(APIView):
#     def get(self, request, pk):
#         try:
#             movie=movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({"error":'Movie not Found'},status=status.HTTP_404_NOT_FOUND)
#         serializer=MovieListSerializers(movie)
#         return Response(serializer.data)
    
#     def put(self,request,pk):
#         movie=Movie.objects.get(pk=pk)
#         serializer=MovieListSerializers(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self,request,pk):
#         movie=Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
                
     
        
class WatchDetailAV(APIView):
    def get(self, request, pk):
        try:
            movie=WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"error":'currently movie not available,We are uploading soon..'},status=status.HTTP_404_NOT_FOUND)
        serializer=WatchListSerializers(movie)
        return Response(serializer.data)
    
    def put(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        serializer=WatchListSerializers(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
                
# streamplatfom 
class StreamplatFormAV(APIView):
    def get(self,request):
        platform=StreamPlatForm.objects.all()
        serializer=StreamPlatFormSerializers(platform, many=True,context={'request':request})  
        return Response(serializer.data)
    
    def post(self,request):
        serializer=StreamPlatFormSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED,context={'request':request})    
        else:
            return Response(serializer.errors)
        
class StreamDetailAV(APIView):
    def get(self, request, pk):
        try:
            platform=StreamPlatForm.objects.get(pk=pk)
        except StreamPlatForm.DoesNotExist:
            return Response({"error":'currently movie not available,We are uploading soon..'},status=status.HTTP_404_NOT_FOUND)
        serializer=StreamPlatFormSerializers(platform,context={'request':request})
        return Response(serializer.data)
    
    def put(self,request,pk):
        movie=StreamPlatForm.objects.get(pk=pk)
        serializer=StreamPlatFormSerializers(movie,data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        movie=StreamPlatForm.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset=Review.objects.all() 
#     serializer_class=ReviewSerializers
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)
     
# class ReviewList(mixins.ListModelMixin,
#                  mixins.CreateModelMixin,
#                  generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializers
    
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
    
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)
        