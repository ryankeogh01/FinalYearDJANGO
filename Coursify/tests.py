import spacy
from django.core.cache import cache
from unittest.mock import patch, Mock
from spacy.tokens import Doc
from django.test import TestCase, Client
from django.urls import reverse
from Coursify.models import Course


class getInterest_Test(TestCase):

    def setUp(self):
        self.client = Client()

    def test_post(self):
        url = reverse('recommender')
        response = self.client.post(url, {'interest': 'sports'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recommendation')
        self.assertTemplateUsed(response, 'recommender.html')

    def test_get(self):
        url = reverse('recommender')
        response= self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recommender.html')


class TestSearchCoursesView(TestCase):
    def test_search_courses_view(self):
        response = self.client.post(reverse('search-courses'), {'searched': 'computer', 'college': ['ABC']})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_course.html')

        course = Course.objects.create(code='TU856', title='Computer Science', college='TUD')
        url = reverse('show-course', args=[course.code])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_course.html')


class RecommenderTest(TestCase):

    def setUpTestData(cls):
        Course.objects.create(title='Mock Course', description='Mock Description')

    def setUp(self):
        cache.clear()

    @patch('Coursify.views.spacy.load')
    def test_recommenderView(self, mock_load):

        mock_nlp = mock_load.return_value
        mock_vocab = spacy.vocab.Vocab()
        mock_nlp.return_value = Doc(mock_vocab, words = ['mock'])
        response = self.client.post(reverse('recommender'), {'interest': 'mock'}, timeout=120)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('results.html')
        print(response.context)
        self.assertContains(response, 'Recommendation Engine')



class GetAverageRentTestCase(TestCase):

    @patch('Coursify.views.requests.get')
    def test_get_average_rent(self, mock_get):
        city_name = 'Dublin'
        country_name = 'Ireland'
        url = reverse('get_average_rent', args=['Dublin', 'Ireland'])
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "prices": [
                {
                    "good_id": 29,
                    "avg": 2000
                }
            ]
        }
        mock_get.return_value = mock_response
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '2000')


class GetAverageSalaryTestCase(TestCase):

    @patch('Coursify.views.requests.get')
    def test_get_average_salary(self, mock_get):
        job_title = 'Software Engineer'
        url = reverse('get_average_salary', args=[job_title])
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "salary_max": 50000,
                },
                {
                    "salary_max": 60000,
                }
            ]
        }
        mock_get.return_value = mock_response
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, '55000')
        print(response)



class TestFavouritesView(TestCase):
    def setUp(self):
        self.client = Client()
        self.course1 = Course.objects.create(code='C001', title='Course 1')
        self.course2 = Course.objects.create(code='C002', title='Course 2')
        self.course3 = Course.objects.create(code='C003', title='Course 3')

    def test_favourites_with_no_cookies(self):
        response = self.client.get(reverse('favourites'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['courses'], [])

    def test_favourites_with_cookies(self):
        cookies = '{"C001": true, "C003": true, "C002": true}'
        response = self.client.get(reverse('favourites'), {'favourites': cookies})
        self.assertEqual(response.status_code, 200)
        expected_codes = ["C001", "C003", "C002"]
        actual_codes = [course.code for course in response.context['courses']]
        print(actual_codes)
        print(response.content)
        self.assertListEqual(actual_codes, expected_codes)

    def tearDown(self):
        self.course1.delete()
        self.course2.delete()
        self.course3.delete()

