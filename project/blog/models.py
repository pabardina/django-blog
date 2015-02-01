from django.db import models
from markdown import markdown


class Article(models.Model):
    """ Article Model """
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=30, unique=True)
    short_content = models.CharField(max_length=250)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    categories = models.ManyToManyField('Category', null=True, blank=True)

    class Meta:
        app_label = 'blog'
        ordering = ['-created_at']

    def save(self):
        self.content = markdown(self.content, ['codehilite'])
        super(Article, self).save()

    def __unicode__(self):
        return self.name


class Category(models.Model):
    """ Category Model """
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    class Meta:
        app_label = 'blog'
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name


class LikePost(models.Model):
    """ LikePost Model """
    article = models.ForeignKey('Article')
    ip = models.IPAddressField()

    class Meta:
        app_label = 'blog'
