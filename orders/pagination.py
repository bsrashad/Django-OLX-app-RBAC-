from rest_framework.pagination import PageNumberPagination

class MyPageNumberPagination(PageNumberPagination):
    
    # page_size = 2  # Number of items per page
    page_size_query_param = 'page_size_num'  # Allow clients to specify page size
    max_page_size = 100  # Maximum number of items per page
