from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _

from task_manager.tasks.models import Task
from task_manager.users.models import User
from django.core.exceptions import ObjectDoesNotExist


class TaskTestWithoutAuth(TestCase):

    def setUp(self):
        self.login = reverse('user_login')
        self.urls = [
            reverse('tasks_list'),
            reverse('task_create'),
            reverse('task_update', kwargs={'pk': 1}),
            reverse('task_delete', kwargs={'pk': 1}),
            reverse('task_detail', kwargs={'pk': 1})
        ]

    def test_no_auth(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertRedirects(response, self.login)


class TaskTestClass(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def setUp(self):
        self.login = reverse('user_login')
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)
        self.tasks = reverse('tasks_list')
        self.task1 = Task.objects.get(pk=2)
        self.task_delete = reverse('task_delete', kwargs={'pk': 5})
        self.form_data = {
            'name': 'new task',
            'status': 8,
            'description': '111',
            'executor': 2,
            'labels': [2, 3, 4]
        }

    def test_task_list(self):
        self.client.force_login(self.user1)
        self.task2 = Task.objects.get(pk=3)
        self.task3 = Task.objects.get(pk=5)
        """
        GET
        """
        response = self.client.get(self.tasks)
        self.assertEqual(response.status_code, 200)
        response_tasks = list(response.context['tasks'])
        self.assertQuerysetEqual(response_tasks,
                                 [self.task1, self.task2,
                                  self.task3])

    def test_task_detail(self):
        self.client.force_login(self.user1)
        self.show_task = reverse('task_detail', kwargs={'pk': 2})
        """
        GET
        """
        response = self.client.get(self.show_task)
        self.assertEqual(response.status_code, 200)
        descriptions = response.context['task']
        self.assertQuerysetEqual(
            [
                descriptions.name,
                descriptions.author,
                descriptions.executor,
                descriptions.description,
                descriptions.status,
                descriptions.created_at,
            ],
            [
                self.task1.name,
                self.task1.author,
                self.task1.executor,
                self.task1.description,
                self.task1.status,
                self.task1.created_at
            ],
        )

    def test_task_create(self):
        self.client.force_login(self.user1)
        self.task_create = reverse('task_create')
        """
        GET
        """
        get_response = self.client.get(self.task_create)
        self.assertEqual(get_response.status_code, 200)
        """
        POST
        """
        post_response = self.client.post(self.task_create,
                                         self.form_data,
                                         follow=True)
        self.assertRedirects(post_response, self.tasks)
        new_task = Task.objects.get(name=self.form_data['name'])
        self.assertEqual(new_task.executor.id, self.user2.id)
        self.assertEqual(new_task.author.id, self.user1.id)
        # self.assertContains(post_response, text='Задача успешно создана')
        self.assertContains(
            post_response,
            text=_('The task was created successfully'))

    def test_task_update(self):
        self.client.force_login(self.user3)
        self.task_update = reverse('task_update', kwargs={'pk': 2})
        """
        GET
        """
        get_response = self.client.get(self.task_update)
        self.assertEqual(get_response.status_code, 200)
        """
        POST
        """
        post_response = self.client.post(self.task_update,
                                         self.form_data,
                                         follow=True)
        self.assertRedirects(post_response, self.tasks)
        self.assertEqual(Task.objects.get(pk=2).executor, self.user2)
        # self.assertContains(post_response, text='Задача успешно изменена')
        self.assertContains(
            post_response,
            text=_('The task updated successfully'))

    def test_own_task_delete(self):
        self.client.force_login(self.user2)
        """
        GET
        """
        get_response = self.client.get(self.task_delete)
        self.assertEqual(get_response.status_code, 200)
        """
        POST
        """
        post_response = self.client.post(self.task_delete, follow=True)
        self.assertRedirects(post_response, self.tasks)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=7)
        # self.assertContains(post_response, text='Задача успешно удалена')
        self.assertContains(
            post_response,
            text=_('The task was successfully deleted'))

    def test_not_own_task_delete(self):
        self.client.force_login(self.user1)
        """
        GET
        """
        get_response = self.client.get(self.task_delete)
        self.assertRedirects(get_response, self.tasks)
        """
        POST
        """
        post_response = self.client.post(self.task_delete, follow=True)
        self.assertRedirects(post_response, self.tasks)
        self.assertEqual(len(Task.objects.all()), 3)

    def test_task_filter(self):
        self.client.force_login(self.user2)
        """
        GET
        """
        content_type_form1 = f'{self.tasks}?status=10&executor=3&label='
        get_response = self.client.get(content_type_form1)
        tasks_list = get_response.context['tasks']
        self.assertEqual(len(tasks_list), 1)
        task = tasks_list[0]
        self.assertEqual(task.name, 'Вторая задача')
        self.assertEqual(task.executor.id, 3)
        self.assertEqual(task.status.id, 10)
        """
        GET (own tasks)
        """
        content_type_form2 = f'{self.tasks}?self_task=on'
        get_response2 = self.client.get(content_type_form2)
        tasks_list = get_response2.context['tasks']
        self.assertEqual(len(tasks_list), 1)
        task = tasks_list[0]
        self.assertEqual(task.name, 'Четвертая задача')
        self.assertEqual(task.author.id, 2)
