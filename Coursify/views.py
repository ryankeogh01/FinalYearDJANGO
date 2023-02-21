import pymongo
import spacy
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import Course
from django.core.paginator import Paginator
from django.db.models import Q
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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





