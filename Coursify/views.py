import pymongo
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import Course
from django.core.paginator import Paginator

def coursePagination(request):
    courses = Course.objects.all()

    p = Paginator(Course.objects.all().order_by('title'), 20)
    page = request.GET.get('page')
    courseList = p.get_page(page)

    return render(request, 'courses.html', {'courseList': courseList})


def search_courses(request):
    course = []
    if request.method == "POST":
        searched = request.POST['searched']
        p = Paginator(Course.objects.filter(title__contains=searched).order_by('title'), 10)
        page = request.GET.get('page')
        course = p.get_page(page)

    return render(request, 'search_course.html', {'courses': course})
    # else:
    #     return render(request, 'search_course.html', {})

# def show_course(request, course_id):
#     course = Course.objects.get(course_id)
#     return render(request, 'show_course.html', {'course': course})

def redirect(request, code):
    try:
        att = Course.objects.get(code=code)
        return render(request, 'show_course.html', {'att': att})
    except:
        return render(request, 'error.html')

#
# def recommender(request):
#     if request.method =='POST'
#     return render(request, 'recommender.html')

def results(request):
    return render(request, 'results.html')


def get_interest(request):
    if request.method == 'POST':
        user_interest = request.POST['interest']
        recommendation = recommender(user_interest)

        return render(request, 'results.html', {'recommendation': recommendation})

    return render(request, 'recommender.html')





