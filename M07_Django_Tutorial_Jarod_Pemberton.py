# this is the code I used following along the Django tutorial for sections Extend You Application and Django Forms. I also did the sections in the extensions to the Django Tutorials Homework-Adding Security to Your Website, Domain, Deploy to Heroku, Homework: Add more to your webstite, and Homework: create comment model

# in blog/templates/blog/post_list.html
<h2><a href="{% url 'post_detail' pk=post.pk %}">{{ post.title }}</a></h2>

# in  blog/urls.py
path('post/<int:pk>/', views.post_detail, name='post_detail'),

# in blog/views.py
from django.shortcuts import render, get_object_or_404

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# in blog/templates/blog/post_detail.html
{% extends 'blog/base.html' %}

{% block content %}
    <article class="post">
        {% if post.published_date %}
            <time class="date">
                {{ post.published_date }}
            </time>
        {% endif %}
        <h2>{{ post.title }}</h2>
        <p>{{ post.text|linebreaksbr }}</p>
    </article>
{% endblock %}

# in gitbash
git status
git add .
git status
git commit -m "Added view and template for detailed blog post as well as CSS for the site."
git push

# in PythonAnywhere command-line
cd ~/jpemberton22.pythonanywhere.com
git pull
workon <your-pythonanywhere-domain>.pythonanywhere.com
python manage.py collectstatic

# in blog/forms.py
from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')

# in blog/templates/blog/base.html
<a href="{% url 'post_new' %}" class="top-menu">
    {% include './icons/file-earmark-plus.svg' %}
</a>

# in blog/urls.py
path('post/new/', views.post_new, name='post_new'),

# in blog/views.py
from .forms import PostForm
def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

# in blog/templates/blog/post_edit.html
{% extends 'blog/base.html' %}

{% block content %}
    <h2>New post</h2>
    <form method="POST" class="post-form">{% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="save btn btn-secondary">Save</button>
    </form>
{% endblock %}

# in blog/views.py
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
    return render(request, 'blog/post_edit.html', {'form': form})

# in blog/templates/blog/post_detail.html
<aside class="actions">
    <a class="btn btn-secondary" href="{% url 'post_edit' pk=post.pk %}">
      {% include './icons/pencil-fill.svg' %}
    </a>
</aside>

# in blog/urls.py
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),

# in blog/views.py
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# in blog/templates/blog/base.html
{% if user.is_authenticated %}
    <a href="{% url 'post_new' %}" class="top-menu">
        {% include './icons/file-earmark-plus.svg' %}
    </a>
{% endif %}

# in blog/templates/blog/post_detail.html
{% if user.is_authenticated %}
     <a class="btn btn-secondary" href="{% url 'post_edit' pk=post.pk %}">
        {% include './icons/pencil-fill.svg' %}
     </a>
{% endif %}

# in gitbash
git status
git add . 
git status 
git commit -m "Added views to create/edit blog post inside the site."
git push

# in PythonAnywhere command-line
cd ~/jpemberton22.pythonanywhere.com
git pull

# in blog/views.py
from django.contrib.auth.decorators import login_required
@login_required
def post_new(request):

# in mysite/urls.py
path('accounts/login/', views.LoginView.as_view(), name='login')

# in blog/templates/registration/login.html
{% extends "blog/base.html" %}

{% block content %}
    {% if form.errors %}
        <p>Your username and password didn't match. Please try again.</p>
    {% endif %}

    <form method="post" action="{% url 'login' %}">
    {% csrf_token %}
        <table>
        <tr>
            <td>{{ form.username.label_tag }}</td>
            <td>{{ form.username }}</td>
        </tr>
        <tr>
            <td>{{ form.password.label_tag }}</td>
            <td>{{ form.password }}</td>
        </tr>
        </table>

        <input type="submit" value="login" />
        <input type="hidden" name="next" value="{{ next }}" />
    </form>
{% endblock %}

# in mysite/settings.py
LOGIN_REDIRECT_URL = '/'

# in blog/templates/blog/base.html
<body>
    <header class="page-header">
        <div class="container">
            {% if user.is_authenticated %}
            <a href="{% url 'post_new' %}" class="top-menu">
                {% include './icons/file-earmark-plus.svg' %}
            </a>
            <a href="{% url 'post_draft_list' %}" class="top-menu">{% include './icons/pencil-square.svg'%}</a>
            {% else %}
            <a href="{% url 'login' %}" class="top-menu">{% include './icons/lock-fill.svg' %}</a>
            {% endif %}
            <h1><a href="/">Django Girls Blog</a></h1>
        </div>
    </header>
    <main class="content container">
        <div class="row">
            <div class="col">
                {% block content %}
                {% endblock %}
            </div>
        </div>
    </main>
</body>

<header class="page-header">
        <div class="container">
            {% if user.is_authenticated %}
            <a href="{% url 'post_new' %}" class="top-menu">
                {% include './icons/file-earmark-plus.svg' %}
            </a>
            <a href="{% url 'post_draft_list' %}" class="top-menu">{% include './icons/pencil-square.svg'%}</a>
            <p id="logout" class="top-menu">Hello {{ user.username }} <small><a href="{% url 'logout' %}">(Log out)</a></small></p>
            {% else %}
            <a href="{% url 'login' %}" class="top-menu">{% include './icons/lock-fill.svg' %}</a>
            {% endif %}
            <h1><a href="/">Django Girls Blog</a></h1>
        </div>
    </header>

# in mysite/urls.py
from django.urls import path, include
from django.contrib import admin

from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', include('blog.urls')),
]

# in blog.css
#logout {
    font-family: 'Lobster', cursive;

}

small a,
small a:hover,
small a:visited {
    font-size: 15pt;
    color: #ffffff;
    text-decoration: none;
}

# I followed along the Domain section

# I could not find any Deploy to Heroku section in the Extentions or in the original Tutorial. It may have been removed.

# in blog/views.py
post.published_date = timezone.now()

# in blog/templates/blog/base.html
<a href="{% url 'post_draft_list' %}" class="top-menu">{% include './icons/pencil-square.svg'%}</a>

# in blog/urls.py
path('drafts/', views.post_draft_list, name='post_draft_list'),

# in blog/views.py
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

# in blog/templates/blog/post_draft_list.html
{% extends 'blog/base.html' %}

{% block content %}
    {% for post in posts %}
        <div class="post">
            <p class="date">created: {{ post.created_date|date:'d-m-Y' }}</p>
            <h1><a href="{% url 'post_detail' pk=post.pk %}">{{ post.title }}</a></h1>
            <p>{{ post.text|truncatechars:200 }}</p>
        </div>
    {% endfor %}
{% endblock %}

# in blog/templates/blog/post_detail.html
{% if post.published_date %}
    <div class="date">
        {{ post.published_date }}
    </div>

    {% else %}
    <aside class="actions">
        <a class="btn btn-secondary" role="button" href="{% url 'post_publish' pk=post.pk %}">Publish</a>
    </aside>
{% endif %}

# in blog/urls.py
path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),

# in blog/views.py
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method=='POST':
        post.publish()
    return redirect('post_detail', pk=pk)

# in blog/templates/blog/post_detail.html
<a class="btn btn-secondary" href="{% url 'post_remove' pk=post.pk %}">
    {% include './icons/trash-fill.svg' %}
</a>

# in blog/urls.py
path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),

# in blog/views.py
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method=='POST':
        post.delete()
    return redirect('post_list')

# in blog/models.py
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

# in PythonAnywhere command-line
python manage.py makemigrations blog
python manage.py migrate blog

# in blog/admin.py
admin.site.register(Comment)
from .models import Post, Comment

# in blog/templates/blog/post_detail.html
<hr>
{% for comment in post.comments.all %}
    <div class="comment">
        <div class="date">{{ comment.created_date }}</div>
        <strong>{{ comment.author }}</strong>
        <p>{{ comment.text|linebreaks }}</p>
    </div>
{% empty %}
    <p>No comments here yet :(</p>
{% endfor %}

# in static/css/blog.css
.comment {
    margin: 20px 0px 20px 20px;
}

# in blog/templates/blog/post_list.html
<a href="{% url 'post_detail' pk=post.pk %}">Comments: {{ post.comments.count }}</a>

# in blog/forms.py
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

from .models import Post, Comment

# in blog/templates/blog/post_detail.html
<a class="btn btn-secondary" role="button" href="{% url 'add_comment_to_post' pk=post.pk %}">Add comment</a>

# in blog/urls.py
path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),

# in blog/views.py
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

from .forms import PostForm, CommentForm

# in blog/templates/blog/add_comment_to_post.html
{% extends 'blog/base.html' %}

{% block content %}
<h1>New comment</h1>
<form method="POST" class="post-form">{% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="save btn btn-secondary">Send</button>
</form>
{% endblock %}

# in blog/templates/blog/post_detail.html
{% for comment in post.comments.all %}
    {% if user.is_authenticated or comment.approved_comment %}
    <div class="comment">
        <div class="date">
            {{ comment.created_date }}
            {% if not comment.approved_comment %}
                <a class="btn btn-default" href="{% url 'comment_remove' pk=comment.pk %}">
                   {% include './icons/hand-thumbs-down.svg' %}
                </a>
                <a class="btn btn-default" href="{% url 'comment_approve' pk=comment.pk %}">
                   {% include './icons/hand-thumbs-up.svg' %}
                </a>
            {% endif %}
        </div>
        <strong>{{ comment.author }}</strong>
        <p>{{ comment.text|linebreaks }}</p>
    </div>
    {% endif %}
{% empty %}
    <p>No comments here yet :(</p>
{% endfor %}

# in blog/urls.py
path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),

# in blog/views.py
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

from .models import Post, Comment
from django.contrib.auth.decorators import login_required

# in blog/templates/blog/post_list.html
<a href="{% url 'post_detail' pk=post.pk %}">Comments: {{ post.approved_comments.count }}</a>

# in blog/models.py
def approved_comments(self):
    return self.comments.filter(approved_comment=True)
