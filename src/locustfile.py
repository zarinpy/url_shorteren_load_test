from faker import Faker
from locust import HttpLocust, between, TaskSequence, seq_task
import random

f = Faker()

urls = [
    "https://docs.locust.io/en/stable/writing-a-locustfile.html",
    "https://stackoverflow.com/questions/9733638/post-json-using-python-requests",
    "https://www.django-rest-framework.org/api-guide/pagination/",
    "https://docs.locust.io/en/stable/",
    "https://bitly.com/",
    "https://docs.locust.io/en/stable/testing-other-systems.html",
    "https://www.django-rest-framework.org/topics/internationalization/",
    "https://www.django-rest-framework.org/api-guide/generic-views/",
    "https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/",
    "https://github.com/encode/django-rest-framework/tree/master",
    "https://github.com/mazdakb/django-naqsh",
    "https://cutt.ly/",
    "https://en.wikipedia.org/wiki/URL_shortening",
    "https://www.rebrandly.com/",
    "https://docs.locust.io/en/stable/increase-performance.html",
    "https://docs.locust.io/en/stable/logging.html#skip-log-setup",
    "https://www.django-rest-framework.org/api-guide/pagination/#setting-the-pagination-style",
    "https://www.django-rest-framework.org/tutorial/3-class-based-views/",
]


class UserTasks(TaskSequence):
    username = None
    password = "test123"
    base_url = 'http://127.0.0.1:8000'
    token = None
    header = {'Content-Type': 'application/json'}
    redirect_to = ''

    @seq_task(1)
    def register(self):
        self.username = f.name().split(' ')
        self.client.post(
            "{0}/api/v1/register/".format(self.base_url), json={
                "username": "".join(self.username),
                "password": self.password,
            }, headers=self.header
        )

    @seq_task(2)
    def get_token(self):
        response = self.client.post(
            "{0}/api/v1/token/".format(self.base_url), json={
                "username": "".join(self.username),
                "password": self.password
            }, headers=self.header
        )
        self.header['Authorization'] = 'Bearer {0}'.format(response.json()['access'])

    @seq_task(3)
    def shorten_url(self):
        response = self.client.post(
            "{0}/api/v1/home/".format(self.base_url), json={
                'base_url': random.choice(urls)
            }, headers=self.header
        )
        self.redirect_to = response.json()['shorted_url']


class WebsiteUser(HttpLocust):
    task_set = UserTasks
    wait_time = between(0.01, 0.1)
