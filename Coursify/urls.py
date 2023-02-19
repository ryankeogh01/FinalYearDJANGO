from django.urls import path

from . import views

urlpatterns = [
    path('courses/', views.coursePagination, name='index'),
    path('refine/', views.search_courses, name='search-courses'),
    path('att/<str:code>/', views.redirect, name='show-course'),
    #path('recommender/', views.recommender, name='recommender'),
    path('results/', views.results, name='results'),
]
