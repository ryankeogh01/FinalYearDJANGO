from django.urls import path

from . import views

urlpatterns = [
    path('courses/', views.coursePagination, name='index'),
    path('refine/', views.search_courses, name='search-courses'),
    path('att/<str:code>/', views.redirect, name='show-course'),
    path('recommender/', views.results, name='recommender'),
    path('results/', views.recommender, name='results'),
    path('salary/<str:job_title>/', views.get_average_salary, name='get_average_salary'),
    path('rent/<str:city_name>/<str:country_name>/', views.get_average_rent, name='get_average_rent'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('favourites/', views.favourites, name='favourites'),

]
