from django.shortcuts import redirect
from django.shortcuts import render
from .models import Post, Ainews
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, AinewsForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import SignupForm
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
import requests


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def error404(request):
    return render(request, "blog/404.html", status=404)


def error500(request):
    return render(request, "blog/500.html", status=500)


def signup(request):  # 역시 GET/POST 방식을 사용하여 구현한다.
    if request.method == "GET":
        return render(request, 'blog/signup.html', {'f': SignupForm()})

    elif request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['password_check']:
                # cleaned_data는 사용자가 입력한 데이터를 뜻한다.
                # 즉 사용자가 입력한 password와 password_check가 맞는지 확인하기위해 작성해주었다.

                new_user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'],
                                                    form.cleaned_data['password'])
                # User.object.create_user는 사용자가 입력한 name, email, password를 가지고 아이디를 만든다.
                # 바로 .save를 안해주는 이유는 User.object.create를 먼저 해주어야 비밀번호가 암호화되어 저장된다.

                new_user.last_name = form.cleaned_data['last_name']
                new_user.first_name = form.cleaned_data['first_name']
                # 나머지 입력하지 못한 last_name과, first_name은 따로 지정해준다.
                new_user.save()

                return HttpResponseRedirect(reverse('vote:index'))
            else:
                return render(request, 'blog/signup.html', {'f': form,
                                            'error': '비밀번호와 비밀번호 확인이 다릅니다.'})

        else:
            return render(request, 'blog/signup.html', {'f': form})


'''
def log_in(request):
'''


def ai_news(request):
    req = requests.get('https://flipboard.com/topic/ai')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    informations = soup.select(
        '#content > div > main > ul > li > div > article > div > h1 > a'
    )

    newslist = []
    for i in range(len(informations)):
        news = Ainews()
        news.title = informations[i].text
        news.text = informations[i].get('href')
        images = soup.select(
            '#content > div > main > ul > li:nth-child(%d) > div > article > div > a > div > img' % (i+1)
        )
        news.image = images[0].get('src')
        newslist.append(news)

    return render(request, 'blog/ai_news.html', {'newslist': newslist})

