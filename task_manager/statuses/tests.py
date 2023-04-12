from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from task_manager.statuses.models import Status
from task_manager.users.models import User


class StatusTestWithoutAuth(TestCase):

    def setUp(self):
        self.login = reverse('user_login')
        self.urls = [
            reverse('statuses_list'),
            reverse('status_create'),
            reverse('status_update', kwargs={'pk': 1}),
            reverse('status_delete', kwargs={'pk': 1})
        ]

    def test_no_auth(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertRedirects(response, self.login)


class StatusTestClass(TestCase):
    fixtures = ['users.json', 'statuses.json',
                'tasks.json', 'labels.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)
        self.statuses = reverse('statuses_list')
        self.form_data = {'name': 'new status'}

    def test_status_list(self):
        self.status1 = Status.objects.get(pk=8)
        self.status2 = Status.objects.get(pk=9)
        self.status3 = Status.objects.get(pk=10)
        response = self.client.get(self.statuses)
        self.assertEqual(response.status_code, 200)
        response_tasks = list(response.context['statuses'])
        self.assertQuerysetEqual(
            response_tasks,
            [
                self.status1,
                self.status2,
                self.status3,
            ],
        )

    def test_status_create(self):
        self.status_create = reverse('status_create')
        """
        GET
        """
        get_response = self.client.get(self.status_create)
        self.assertEqual(get_response.status_code, 200)
        """
        POST
        """
        post_response = self.client.post(self.status_create,
                                         self.form_data,
                                         follow=True)
        self.assertRedirects(post_response, self.statuses)
        self.assertTrue(Status.objects.get(id=11))
        self.assertContains(post_response,
                            _('The status was created successfully'))

    def test_status_update(self):
        self.status_update = reverse('status_update', kwargs={'pk': 8})
        """
        GET
        """
        get_response = self.client.get(self.status_update)
        self.assertEqual(get_response.status_code, 200)
        """
        POST
        """
        post_response = self.client.post(self.status_update,
                                         self.form_data,
                                         follow=True)
        self.assertRedirects(post_response, self.statuses)
        self.status = Status.objects.get(pk=8)
        self.assertEqual(self.status.name, self.form_data['name'])
        self.assertContains(post_response,
                            _('The status updated successfully'))

    def test_not_used_status_delete(self):
        self.status_delete = reverse('status_delete', kwargs={'pk': 9})
        """
        GET
        """
        get_response = self.client.get(self.status_delete)
        self.assertEqual(get_response.status_code, 200)
        """
        POST
        """
        post_response = self.client.post(self.status_delete,
                                         follow=True)
        self.assertRedirects(post_response, self.statuses)
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=9)
        self.assertContains(post_response,
                            _('The status was successfully deleted'))

    def test_used_status_delete(self):
        self.status_delete = reverse('status_delete', kwargs={'pk': 8})
        """
        GET
        """
        get_response = self.client.get(self.status_delete)
        self.assertEqual(get_response.status_code, 200)
        """
        POST
        """
        post_response = self.client.post(self.status_delete)
        self.assertRedirects(post_response, self.statuses)
        self.assertEqual(len(Status.objects.all()), 3)
