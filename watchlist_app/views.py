from watchlist_app.models import *
from django.http import JsonResponse
def movie_list(request):
    movies = Movie.objects.all()
    # print(list(movies.values()))
    # return JsonResponse({'movies':movies})
    data={'movies':list(movies.values())}
    return JsonResponse(data)

# movie details 
def movie_detail(request ,pk):
    movie=Movie.objects.get(pk=pk) 
    # specific object will be displayed 
    data={
        'name':movie.name,
        'description':movie.description,
        'active':movie.active
    }
    return JsonResponse(data)