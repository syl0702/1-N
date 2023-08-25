from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm, CommentForm

# Create your views here.
def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles,
    }

    return render(request, 'index.html', context)

def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = ArticleForm()

    context = {
        'form': form,
    }

    return render(request, 'form.html', context)

def detail(request, id):
    article = Article.objects.get(id=id)
    comment_form = CommentForm()

    context = {
        'article': article,
        'comment_form': comment_form,
    }

    return render(request, 'detail.html', context)

def comment_create(request, article_id):
    # 사용자가 입력한 정보를 form에 입력
    comment_form = CommentForm(request.POST)

    # 유효성 검사
    if comment_form.is_valid():
        # form을 저장 => 추가로 넣어야 하는 데이터를 넣기 위해 저장 멈춰!
        comment = comment_form.save(commit=False)

        # 첫번째 방법.
        # article_id를 기준으로 article object를 가져와서
        # article = Article.objects.get(id=article_id)
        # # article 컬럼에 추가
        # comment.article = article

        # 두번째 방법.
        comment.article_id = article_id
        

        # 저장
        comment.save()

        return redirect('articles:detail', id=article_id) 