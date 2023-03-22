from unittest.mock import patch

import spacy
from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse
from unittest import mock

from spacy.tokens import Doc

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

    # def test_resultsPage(self):
    #     response = self.client.get(reverse('results'), {'recommender_results': [('Mock Course', 0.8)]})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed('results.html')
    #     self.assertContains(response, 'Mock Course')
    #     self.assertContains(response, '0.8')
    #
    #     # Check that at least one recommended course is displayed
    #     recommender_results = response.context['recommender_results']
    #     self.assertTrue(len(recommender_results) > 0)
    #
    # @patch('Coursify.views.spacy.load')
    # def test_dataCleaning(self, mock_load):
    #     mock_nlp = mock_load.return_value
    #     mock_vocab = spacy.vocab.Vocab()
    #     mock_nlp.return_value = Doc(mock_vocab, words=['mock'])
    #     clean_desc_str = 'mock description'
    #     courses = [Course(title='Mock Course', description='Mock Description'),
    #                Course(title='Mock Course 2', description='Mock Description 2'),
    #                Course(title='Mock Course 3', description='Mock Description 3')]
    #     expected_descriptions = {clean_desc_str: courses[0]}
    #     with patch.object(Course.objects, 'all', return_value=courses):
    #         with patch.object(spacy, 'load', return_value=mock_nlp):
    #             response = self.client.post(reverse('recommender'), {'interest': 'mock'})
    #             self.assertEqual(response.status_code, 200)
    #             self.assertIn(cache.get('cleaned_course_descriptions'), expected_descriptions)


# Create your tests here.
from unittest.mock import patch, Mock

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
        mock_get.assert_called_once_with(f'https://cost-of-living-and-prices.p.rapidapi.com/prices?city_name={city_name}&country_name={country_name}', headers={
            'X-RapidAPI-Key': '482b4d75edmsha168474ea6b6d1ap1640bbjsn3d6e5bca623a',
            'X-RapidAPI-Host': 'cost-of-living-and-prices.p.rapidapi.com'
        })



