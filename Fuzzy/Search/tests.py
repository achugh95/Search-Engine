from django.test import TestCase
from django.urls import reverse, resolve

#  Create your tests here.


class TestUrls(TestCase):

    # Query
    def test_query(self):
        url = reverse('query')
        # print(url)
        assert resolve(url).view_name == 'query'

    # Search API 
    def test_search_service(self):
        url = reverse('search service')
        print(url)
        assert resolve(url).view_name == 'search service'

