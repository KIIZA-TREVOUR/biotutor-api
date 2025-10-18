from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Category, BiologyContent

# Create your tests here.
User = get_user_model()
class BiologyContentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create users
        self.teacher = User.objects.create_user(
            username='teacher1', password='pass123', role='teacher'
        )
        self.student = User.objects.create_user(
            username='student1', password='pass123', role='student'
        )
        
        # Create category
        self.category = Category.objects.create(
            name='Cells', slug='cells', description='Cell biology'
        )
        
        # Create content
        self.published = BiologyContent.objects.create(
            title='Published Lesson', slug='pub', summary='Summary',
            content_body='Body', is_published=True,
            author=self.teacher, category=self.category
        )
        self.draft = BiologyContent.objects.create(
            title='Draft Lesson', slug='draft', summary='Draft',
            content_body='Draft body', is_published=False,
            author=self.teacher, category=self.category
        )

    def test_student_sees_only_published(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/content/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Published Lesson')

    def test_teacher_sees_own_content(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get('/api/content/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)  

    def test_filter_by_category(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/content/?category=cells')
        self.assertEqual(len(response.data['results']), 1)