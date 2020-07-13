from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render

from django.views.generic import ListView,   CreateView
from django.utils.decorators import method_decorator

# Create your views here.
from .tasks import save_comment
from .forms import ArticleForm
from .models import Article, Comment


@method_decorator(login_required, name='dispatch')
class ArticlesListView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'home.html'
    paginate_by = 5

    def get_queryset(self):
        self.article = Article.objects.all()
        qs = self.article.order_by('-created_at')
        return qs


@login_required
def handle_article_detail(request, pk, *args, **kwargs):
    context = {}
    context['article'] = get_object_or_404(Article, pk=pk)
    user_id = request.user.id
    page = request.GET.get('page', 1)

    if request.method == 'POST' and request.is_ajax():
        comment = request.POST.get('comment')
        try:
            parent_id = int(request.POST.get('parent'))
        except ValueError:
            parent_id = None
        save_comment.delay(comment, pk, user_id, parent_id,)
    else:
        comments_list = Comment.objects.filter(
            article=context['article'],
            reply__isnull=True).order_by('-created_at')
        paginator = Paginator(comments_list, 5)
        try:
            context['comments'] = paginator.page(page)
        except PageNotAnInteger:
            context['comments'] = paginator.page(1)
        except EmptyPage:
            context['comments'] = paginator.page(paginator.num_pages)
    return render(request, 'article.html', context)


@method_decorator(login_required, name='dispatch')
class CreateArticleView(CreateView):
    template_name = 'new_article.html'
    form_class = ArticleForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateArticleView, self).form_valid(form)
