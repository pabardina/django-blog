from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blog.models import Article, Category
from markdown import markdown
from django.contrib.auth.models import User


class PostTest(TestCase):
    def test_create_article(self):
        # Create the post
        post = Article()

        # Set the attributes
        post.name = 'My first post'
        post.slug = 'my-first-post'
        post.short_content = 'This is my first blog post'
        post.content = 'blablabla'
        post.published = True
        post.created_at = timezone.now()
        post.updated_at = timezone.now()

        # Save it
        post.save()

        # Check we can find it
        all_posts = Article.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Check attributes
        self.assertEquals(only_post.name, 'My first post')
        self.assertEquals(only_post.slug, 'my-first-post')
        self.assertEquals(only_post.short_content, 'This is my first blog post')
        self.assertEquals(only_post.content, markdown('blablabla'))
        self.assertEquals(only_post.created_at, post.created_at)
        self.assertEquals(only_post.updated_at, post.updated_at)


class AdminTest(LiveServerTestCase):
    # fixtures = ['users.json']

    def setUp(self):
        self.user = User(
            username='michel', email='test@example.com', is_active=True,
            is_staff=True, is_superuser=True,
        )
        self.user.set_password('blanc')
        self.user.save()
        self.client.login(username='michel', password='blanc')

    def test_login(self):
        # Create client
        c = Client()

        # Get login page
        response = c.get('/admin/', follow=True)

        # Check response code
        self.assertEquals(response.status_code, 200)

        # Check 'Log in' in response
        self.assertTrue(b'Log in' in response.content)

        # Log the user in
        c.login(username='michel', password="blanc")

        # Check response code
        response = c.get('/admin/')
        self.assertEquals(response.status_code, 200)

        # Check 'Log out' in response
        self.assertTrue(b'Log out' in response.content)

    def test_logout(self):
        # log in
        self.client.login(username="michel", password="blanc")

        # check reponse code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)

        # Check 'Log out' in response
        self.assertTrue(b'Log out' in response.content)

        # Log out
        self.client.logout()

        # Check response code
        response = self.client.get('/admin/', follow=True)
        self.assertEquals(response.status_code, 200)

        # Check 'Log in' in response
        self.assertTrue(b'Log in' in response.content)

    def test_create_post(self):
        # Log in
        self.client.login(username='michel', password="blanc")

        # Check response code
        response = self.client.get('/admin/blog/article/add/')
        self.assertEquals(response.status_code, 200)

        # Create the new post
        response = self.client.post('/admin/blog/article/add/', {
            'name': 'My first post',
            'slug': 'my_first_post',
            'short_content': 'This is my first post',
            'content': 'This is my first post',
            'published': 1,
        }, follow=True)

        self.assertEquals(response.status_code, 200)

        # Check added successfully
        self.assertTrue(b'Select article to change' in response.content)

        # Check new post now in database
        all_posts = Article.objects.all()
        self.assertEquals(len(all_posts), 1)

    def test_edit_post(self):
        # Create the post
        post = Article()
        post.name = 'My first post'
        post.slug = 'my-first-post'
        post.short_content = 'This is my first blog post'
        post.content = 'This is my first blog post'
        post.published = True
        post.save()

        # Log in
        self.client.login(username='michel', password="blanc")

        # Edit the post
        response = self.client.post('/admin/blog/article/3/', {
            'name': 'My second post',
            'slug': 'my-second-post',
            'short_content': 'This is my second blog post',
            'content': 'This is my second blog post',
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check changed successfully
        self.assertTrue(b'Select article to change' in response.content)

        # Check post amended
        all_posts = Article.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post.name, 'My second post')
        self.assertEquals(only_post.content,
                          markdown('This is my second blog post'))

    def test_delete_post(self):
        # Create the post
        post = Article()
        post.name = 'My first post'
        post.slug = 'my-first-post'
        post.short_content = 'This is my first blog post'
        post.content = 'This is my first blog post'
        post.published = True
        post.save()

        # Check new post saved
        all_posts = Article.objects.all()
        self.assertEquals(len(all_posts), 1)

        # Log in
        self.client.login(username='michel', password="blanc")

        # Delete the post
        response = self.client.post('/admin/blog/article/2/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue(b'Select article to change' in response.content)

        # Check post amended
        all_posts = Article.objects.all()
        self.assertEquals(len(all_posts), 0)


class PostViewTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()

    def test_index(self):
        # Create the post
        post = Article()
        post.name = 'My first post'
        post.slug = 'my-first-post'
        post.short_content = 'This is my first blog post'
        post.content = 'This is my first blog post'
        post.published = True
        post.save()

        # Check new post saved
        all_posts = Article.objects.filter(published=True)
        self.assertEquals(len(all_posts), 1)

        # Fetch the index
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

        # Check the post title is in the response
        self.assertTrue(b'My first post' in response.content)

        # Check the post text is in the response
        self.assertTrue(b'This is my first' in response.content)