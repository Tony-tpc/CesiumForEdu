from audioop import reverse

from django.test import TestCase, Client
from .models import Topic , FirstLevelBranch, SecondLevelBranch, ThirdLevelBranch, FourthLevelBranch

class TopicModelTest(TestCase):
    def setUp(self):
        self.client = Client()

    def create_topic_success(self):
        url = reverse('neo4jDB:create_topic')