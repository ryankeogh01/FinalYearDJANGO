import spacy
from django.http import JsonResponse
from django.core.cache import cache

from django.shortcuts import render
from .models import Course
from django.core.paginator import Paginator
import requests
from django.http import HttpResponseServerError



def coursePagination(request):
    p = Paginator(Course.objects.all().order_by('title'), 20)
    page = request.GET.get('page')
    courseList = p.get_page(page)

    return render(request, 'courses.html', {'courseList': courseList})



def search_courses(request):
    if request.method == 'POST':
        try:
            college = request.POST.getlist('college')
            if college:
                searched = request.POST['searched']
                course = Course.objects.filter(title__icontains=searched, college__in=college).order_by('title')
                return render(request, 'search_course.html', {'course': course})
            else:
                searched = request.POST['searched']
                course = Course.objects.filter(title__icontains=searched).order_by('title')
                return render(request, 'search_course.html', {'course': course})
        except Exception as e:
            return HttpResponseServerError(f"Error on course search: {e}")


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


def recommender(request):
    if request.method == 'POST':
        user_interest = request.POST.get('interest')

        nlp = spacy.load('en_core_web_lg')

        if cache.get('cleaned_course_descriptions') is not None:
            course_descriptions = cache.get('cleaned_course_descriptions')
        else:
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

            cache.set('cleaned_course_descriptions', course_descriptions, timeout=None)
        similarity_scores = []

        for desc in course_descriptions:
            doc1 = nlp(user_interest)
            doc2 = nlp(desc)
            similarity_scores.append(doc1.similarity(doc2))

        recommended_courses = []
        for idx, score in sorted(enumerate(similarity_scores), key=lambda x: x[1], reverse=True)[:20]:
            desc = list(course_descriptions.keys())[idx]
            recommended_course = course_descriptions[desc]
            recommended_courses.append((recommended_course, score))

        return render(request, 'results.html', {'recommender_results': recommended_courses})


def get_average_salary(request, job_title=''):
    if job_title:
        api_key = '84f2871a1c31d44cecbdafa994936b34'
        app_id = '14541fa5'
        url = f'https://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={app_id}&app_key={api_key}&what={job_title}&content-type=application/json'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data['results']:
                salary_max_values = [result['salary_max'] for result in data['results'] if result['salary_max']]
                if salary_max_values:
                    average_salary = sum(salary_max_values) / len(salary_max_values)
                    average_salary = str(round(average_salary, -3))
                    return render(request, 'home.html', {'average_salary': average_salary})
                else:
                    error_message_salary = f"No salary data found for {job_title}"
                    return render(request, 'home.html', {'error_message_salary': error_message_salary})
            else:
                error_message_salary = f"No jobs found for {job_title}"
                return render(request, 'home.html', {'error_message_salary': error_message_salary})
        else:
            error_message_salary = f"Error {response.status_code}: {response.reason}"
            return render(request, 'home.html', {'error_message_salary': error_message_salary})

    else:
        error_message_salary = "Please enter a Job Title "
        return render(request, 'home.html', {'error_message_salary': error_message_salary})


def get_average_rent(request, city_name='', country_name=''):
    if city_name and country_name:

        headers = {
            'X-RapidAPI-Key': '482b4d75edmsha168474ea6b6d1ap1640bbjsn3d6e5bca623a',
            'X-RapidAPI-Host': 'cost-of-living-and-prices.p.rapidapi.com'
        }
        url = f'https://cost-of-living-and-prices.p.rapidapi.com/prices?city_name={city_name}&country_name={country_name}'
        response = requests.get(url, headers=headers)
        code = response.status_code

        if code == 200:
            data = response.json()
            if 'error' in data and data['error']:
                error_message = f"No rent data found for {city_name}, {country_name}"
                return render(request, 'home.html', {'error_message': error_message})

            if data['prices']:
                for item in data['prices']:
                    if item['good_id'] == 29:
                        average_rent = item['avg']
                        return render(request, 'home.html', {'average_rent': average_rent})
                    else:
                        error_message = f"No rent data found for {city_name}, {country_name}"

        else:
            error_message = f"Error {code}: {response.reason}"
    else:
        error_message = "Please enter a city and country name"

    return render(request, 'home.html', {'error_message': error_message})


def autocomplete(request):
    query = request.GET.get("searched", "")
    courses = Course.objects.filter(title__icontains=query).distinct()[:20]
    course_title = [course.title for course in courses]
    return JsonResponse(course_title, safe=False)


def favourites(request):
    courses =[]
    if 'favourites' in request.COOKIES:
        favourites = request.COOKIES['favourites']
        codes = [code.replace('"', '').replace(':true', '') for code in favourites.strip('{}').split(',')]
        courses = Course.objects.filter(code__in=codes)
    return render(request, 'favourites.html', {'courses': courses})


