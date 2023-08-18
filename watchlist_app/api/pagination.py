from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size=0
    page_query_param='p'
    page_size_query_param='size'
    max_page_size=10
    last_page_string='end'

class watchLpagination(LimitOffsetPagination):
    default_limit=5
    page_size=3
    limit_query_param='param'
    
class WatchCpagination(CursorPagination):
    page_size=4
    cursor_query_param="record"
    ordering='-created'
    