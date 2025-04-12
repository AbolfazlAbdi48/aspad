import feedparser
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView

from blog_module.models import Article


# Create your views here.
class BlogListView(ListView):
    model = Article
    queryset = Article.objects.filter(status='p', publish_time__lte=timezone.now())[:3]
    template_name = 'blog/blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        zoomit_feed = feedparser.parse('https://www.zoomit.ir/feed/')
        digiato_feed = feedparser.parse('https://digiato.com/feed')

        context['zoomit_articles'] = zoomit_feed.entries[:20]
        context['digiato_articles'] = digiato_feed.entries[:20]

        return context


class BlogDetailView(DetailView):
    model = Article
    template_name = 'blog/blog_detail.html'

    def get_queryset(self):
        return Article.objects.filter(status='p', publish_time__lte=timezone.now(), id=self.kwargs.get('pk'))
