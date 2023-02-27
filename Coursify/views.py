import spacy

from django.shortcuts import render
from .models import Course
from django.core.paginator import Paginator
import requests


def coursePagination(request):
    courses = Course.objects.all()

    p = Paginator(Course.objects.all().order_by('title'), 20)
    page = request.GET.get('page')
    courseList = p.get_page(page)

    return render(request, 'courses.html', {'courseList': courseList})


# def course_searchPagination(request):
#     courses = Course.objects.all()
#
#     p = Paginator(Course.objects.all().order_by('title'), 20)
#     page = request.GET.get('page')
#     courseList = p.get_page(page)
#
#     return render(request, 'search_course.html', {'courseList': courseList})


def search_courses(request):
    searched = request.POST['searched']
    course = Course.objects.filter(title__contains=searched).order_by('title')

    return render(request, 'search_course.html', {'course': course})



def redirect(request, code):
    try:
        att = Course.objects.get(code=code)
        return render(request, 'show_course.html', {'att': att})
    except:
        return render(request, 'error.html')

def results(request):
    return render(request, 'recommender.html')

def get_interest(request):
    if request.method == 'POST':
        user_interest = request.POST['interest']
        recommendation = recommender(user_interest)

        return render(request, 'results.html', {'recommendation': recommendation})

    return render(request, 'recommender.html')



# def recommender(request):
#     if request.method == 'POST':
#         user_interest = request.POST.get('interest')
#
#         nlp = spacy.load('en_core_web_lg')
#
#         course_descriptions = Course.objects.values_list('description', flat=True)
#
#
#         similarity_scores = []
#
#         for course_description in course_descriptions:
#             if course_description is not None:
#                 doc1 = nlp(user_interest)
#                 doc2 = nlp(course_description)
#                 similarity_scores.append(doc1.similarity(doc2))
#
#         recommended_courses = []
#         for idx, score in sorted(enumerate(similarity_scores), key=lambda x:x[1], reverse=True)[:20]:
#             recommended_course = Course.objects.filter(description=course_descriptions[idx]).first()
#             if recommended_course:
#                 recommended_courses.append((recommended_course, score))
#
#         return render(request, 'results.html', {'recommender_results': recommended_courses})


def recommender(request):
    if request.method == 'POST':
        user_interest = request.POST.get('interest')

        nlp = spacy.load('en_core_web_lg')

        courses = Course.objects.all()
        course_descriptions = {}

        for course in courses:
            if course.description is not None:
                description = nlp(course.description.lower())
                clean_desc = []
                for token in description:
                    if not token.is_punct and not token.is_currency and not token.is_digit and not token.is_oov \
                            and not token.is_space and not token.is_stop and not token.like_num and token.pos_ != "PROPN":
                        clean_desc.append(token.lemma_)
                clean_desc_str = ' '.join(clean_desc)
                course_descriptions[clean_desc_str] = course

        similarity_scores = []

        for desc in course_descriptions:
            doc1 = nlp(user_interest)
            doc2 = nlp(desc)
            similarity_scores.append(doc1.similarity(doc2))

        recommended_courses = []
        for idx, score in sorted(enumerate(similarity_scores), key=lambda x:x[1], reverse=True)[:20]:
            desc = list(course_descriptions.keys())[idx]
            recommended_course = course_descriptions[desc]
            recommended_courses.append((recommended_course, score))

        return render(request, 'results.html', {'recommender_results': recommended_courses})







# def get_average_salary(request):
#     if request.method == 'POST':
#         job_title = request.POST.get('job-title')
#         api_key = '84f2871a1c31d44cecbdafa994936b34'
#         app_id = '14541fa5'
#         url = f'https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id}&app_key={api_key}&what={job_title}&content-type=application/json'
#         response = requests.get(url)
#         data = response.json()
#         average_salary = data['results'][0]['salary_max']
#         return render(request, 'home.html', {'average_salary': average_salary})
#     else:
#         return render(request, 'home.html')

def get_average_salary(request, job_title=''):
    if job_title:
        api_key = '84f2871a1c31d44cecbdafa994936b34'
        app_id = '14541fa5'
        url = f'https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id}&app_key={api_key}&what={job_title}&content-type=application/json'
        response = requests.get(url)
        data = response.json()
        average_salary = data['results'][0]['salary_max'] + data['results'][1]['salary_max'] /2
    else:
        average_salary = None
    return render(request, 'home.html', {'average_salary': average_salary})






