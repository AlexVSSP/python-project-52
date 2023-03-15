from django.test import TestCase

from task_manager.users.models import User
from django.urls import reverse


class UserModelTest(TestCase):

    def setUp(self):
        User.objects.create(username='Ace Ventura', first_name='Jim',
                            last_name='Carrey')

    def test_user_full_name(self):
        user = User.objects.get(id=1)
        expected_full_name = '%s %s' % (user.first_name, user.last_name)
        self.assertEquals(expected_full_name, str(user))


class IndexViewTest(TestCase):

    def setUp(self):
        User.objects.create(username='Ace Ventura', first_name='Jim',
                            last_name='Carrey')
        User.objects.create(username='Frank Drebin', first_name='Leslie',
                            last_name='Nielsen')
        User.objects.create(username='Jackie', first_name='Jackie',
                            last_name='Chan')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'users/users.html')

    def test_lists_all_users(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['users']) == 3)


class UserTestClass(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)
        self.form_data = {
            'username': 'Spitfire',
            'first_name': 'Stas',
            'last_name': 'Tihomirov',
            'password1': 'yanenoob',
            'password2': 'yanenoob',
        }

    def test_user_create(self):
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')
        request = self.client.post(reverse('user_create'), self.form_data,
                                   follow=True)
        self.assertRedirects(request, reverse('user_login'))
        self.assertContains(request, 'Пользователь успешно зарегистрирован')
        self.assertTrue(User.objects.get(pk=4))

    def test_user_update_success(self):
        self.client.force_login(self.user3)
        response = self.client.get(reverse('user_update', kwargs={"pk": 3}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')
        request = self.client.post(reverse('user_update', kwargs={"pk": 3}),
                                   self.form_data, follow=True)
        self.assertRedirects(request, reverse('users_list'))
        updated_user = User.objects.get(pk=3)
        self.assertEqual(updated_user.username, self.form_data['username'])
        self.assertContains(request, 'Пользователь успешно изменен')

    def test_user_update_no_permission(self):
        self.client.force_login(self.user3)
        updated_user = reverse('user_update', kwargs={"pk": 2})
        get_response = self.client.get(updated_user, follow=True)
        self.assertRedirects(get_response, reverse('users_list'))
        post_response = self.client.get(updated_user, self.form_data,
                                        follow=True)
        user = User.objects.get(pk=2)
        self.assertRedirects(post_response, reverse('users_list'))
        self.assertFalse(user.username == self.form_data['username'])
        self.assertContains(post_response,
                            'У вас недостаточно прав, '
                            'чтобы редактировать другого пользователя')

    def test_user_delete_success(self):
        self.client.force_login(self.user3)
        deleted_user = reverse('user_delete', kwargs={"pk": 3})
        get_response = self.client.get(deleted_user, follow=True)
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, 'users/delete.html')
        post_response = self.client.post(deleted_user, follow=True)
        self.assertRedirects(post_response, reverse('users_list'))
        self.assertContains(post_response, 'Пользователь успешно удален')

    def test_user_delete_no_permission(self):
        self.client.force_login(self.user3)
        deleted_user = reverse('user_delete', kwargs={"pk": 2})
        get_response = self.client.get(deleted_user, follow=True)
        self.assertEqual(get_response.status_code, 200)
        self.assertRedirects(get_response, reverse('users_list'))
        self.assertEqual(len(User.objects.all()), 3)
        post_response = self.client.post(deleted_user, follow=True)
        self.assertContains(post_response,
                            'У вас недостаточно прав, '
                            'чтобы редактировать другого пользователя')
