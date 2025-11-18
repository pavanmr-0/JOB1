from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser
from companies.models import Company


class CompaniesFunctionalTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_company_view(self):
        user = CustomUser.objects.create_user(username='employer1', password='pass', role='employer')
        self.client.login(username='employer1', password='pass')

        url = reverse('companies:create_company')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        data = {
            'company_name': 'TestCo',
            'description': 'A test company',
            'location': 'Test City',
            'website': 'https://example.com',
            'established_year': '2000',
        }
        resp = self.client.post(url, data)
        self.assertIn(resp.status_code, (302, 303))
        company = Company.objects.filter(company_name='TestCo').first()
        self.assertIsNotNone(company)
        self.assertEqual(company.owner, user)
