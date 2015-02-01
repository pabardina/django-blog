from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from blog.models import Category, Article, LikePost
import calendar, datetime
from django.http import HttpResponse
from blog.utils import get_client_ip


def list_articles(request):
    """ List Articles """

    page = request.GET.get('page')
    article_queryset = Article.objects.filter(published=True)
    paginator = Paginator(article_queryset, 10)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    return render(
        request,
        "articles.html",
        {
            "articles": articles,
        }
    )


def article(request, slug):
    """A single article"""

    article = get_object_or_404(Article, slug=slug)
    ip = get_client_ip(request)
    like = LikePost.objects.filter(article=article, ip=ip).first()
    return render(
        request,
        "article.html", {
            "article": article,
            "like": like
        }
    )


def like(request, id):
    article = get_object_or_404(Article, id=id)
    ip = get_client_ip(request)
    if not LikePost.objects.filter(article=article, ip=ip):
        like = LikePost.objects.create(article=article, ip=ip)
        return HttpResponse("success")
    else:
        return HttpResponse("already like")
