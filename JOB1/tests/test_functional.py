from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser, Profile
from companies.models import Company
from django.core.files.uploadedfile import SimpleUploadedFile


class FunctionalTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_company_view(self):
        # create an employer user
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
        # simulate posting with no file
        resp = self.client.post(url, data)
        # after successful create, view redirects to company_profile
        self.assertIn(resp.status_code, (302, 303))
        # company should be created
        company = Company.objects.filter(company_name='TestCo').first()
        self.assertIsNotNone(company)
        self.assertEqual(company.owner, user)

    def test_resume_builder_view(self):
        user = CustomUser.objects.create_user(username='seeker1', password='pass', role='job_seeker')
        self.client.login(username='seeker1', password='pass')

        url = reverse('resume_builder:resume_builder')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        resume_file = SimpleUploadedFile('resume.txt', b'Test resume content')
        data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'location': 'City',
        }
        resp = self.client.post(url, data, follow=True, FILES={'resume': resume_file})
        # should render preview or redirect; ensure no server error
        self.assertLess(resp.status_code, 500)
        # profile resume should be saved
        profile = Profile.objects.filter(user=user).first()
        self.assertIsNotNone(profile)
        self.assertTrue(bool(profile.resume))
