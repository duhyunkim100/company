from django.urls import path
from networkapp.views import search_company, network_view

urlpatterns = [
    # 기본 검색 페이지
    path("", search_company, name="search_company"),
    
    # 네트워크 시각화 페이지
    path('network/<str:company_name>/', network_view, name='network_view'),
    
]