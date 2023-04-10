from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from task_manager.labels.models import Label
from task_manager.users.models import User


class LabelTestWithoutAuth(TestCase):

    def setUp(self):
        self.login = reverse('user_login')
        self.urls = [
            reverse('labels_list'),
            reverse('label_create'),
            reverse('label_update', kwargs={'pk': 1}),
            reverse('label_delete', kwargs={'pk': 1})
        ]

    def test_no_auth(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertRedirects(response, self.login)


class LabelTestClass(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def setUp(self):
        self.user = User.objects.get(pk=2)
        self.client.force_login(self.user)
        self.labels = reverse('labels_list')
        self.form_data = {'name': 'new label'}

    def test_label_list(self):
        response = self.client.get(self.labels)
        self.assertEqual(response.status_code, 200)
        labels = list(response.context['labels'])
        self.assertEqual(len(labels), 3)
        label1 = labels[0]
        self.assertEqual(label1.name, 'Пупер')

    def test_label_create(self):
        self.label_create = reverse('label_create')
        """
        GET
        """
        get_response = self.client.get(self.label_create)
        self.assertEqual(get_response.status_code, 200)
        """
        POST
        """
        post_response = self.client.post(self.label_create,
                                         self.form_data,
                                         follow=True)
        self.assertRedirects(post_response, self.labels)
        new_label = Label.objects.get(name=self.form_data['name'])
        self.assertEqual(new_label.id, 5)
        # self.assertContains(post_response, 'Метка успешно создана')
        self.assertContains(post_response,
                            _('The label was created successfully'))

    def test_label_update(self):
        self.label_update = reverse('label_update', kwargs={'pk': 2})
        """
        GET
        """
        get_response = self.client.get(self.label_update)
        self.assertEqual(get_response.status_code, 200)
        """
        POST
        """
        post_response = self.client.post(self.label_update,
                                         self.form_data,
                                         follow=True)
        self.assertRedirects(post_response, self.labels)
        updated_label = Label.objects.get(pk=2)
        self.assertEqual(updated_label.name, 'new label')
        # self.assertContains(post_response, 'Метка успешно изменена')
        self.assertContains(post_response, _('The label updated successfully'))

    def test_not_used_label_delete(self):
        self.label_delete = reverse('label_delete', kwargs={'pk': 3})
        """
        GET
        """
        get_response = self.client.get(self.label_delete, follow=True)
        self.assertEqual(get_response.status_code, 200)
        """
        POST
        """
        post_response = self.client.post(self.label_delete, follow=True)
        self.assertRedirects(post_response, self.labels)
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(pk=3)
        # self.assertContains(post_response, 'Метка успешно удалена')
        self.assertContains(post_response,
                            _('The label was successfully deleted'))

    def test_used_label_delete(self):
        self.label_delete = reverse('label_delete', kwargs={'pk': 2})
        """
        GET
        """
        get_response = self.client.get(self.label_delete, follow=True)
        self.assertEqual(get_response.status_code, 200)
        """
        POST
        """
        post_response = self.client.post(self.label_delete, follow=True)
        self.assertRedirects(post_response, self.labels)
        self.assertEqual(len(Label.objects.all()), 3)
