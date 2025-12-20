# this is the code that I had used for the M05 Django tutorial

git init
git config --global user.name "Jarod"
git config --global user.email jpemberton22@ivytech.edu

# in .gitignore
# Python
*.pyc
*~
__pycache__

# Env
.env
myvenv/
venv/

# Database
db.sqlite3

# Static folder at project root
/static/

# macOS
._*
.DS_Store
.fseventsd
.Spotlight-V100

# Windows
Thumbs.db*
ehthumbs*.db
[Dd]esktop.ini
$RECYCLE.BIN/

# Visual Studio
.vscode/
.history/
*.code-workspace

# in gitbash
git status
git add .
git commit -m "My Django Girls app, first commit"
git remote add origin https://github.com/jpemberton22/my-first-blog.git
git push -u origin HEAD

# in PytonAnywhere command-line
pip3.10 install --user pythonanywhere
pa_autoconfigure_django.py --python=3.10 https://github.com/jpemberton22/my-first-blog.git
python manage.py createsuperuser
ls
ls blog/

# in mysite/urls.py
path('', include('blog.urls')),

# in blog/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('', views.post_list, name='post_list'),
]

# in blog/views.py
def post_list(request):
    return render(request, 'blog/post_list.html', {})

# in blog/templates/blog/post_list.html
<!DOCTYPE html>
<html>
<body>
    <p>Hi there!</p>
    <p>It works!</p>
</body>
</html>

<!DOCTYPE html>
<html>
    <head>
        <title>Ola's blog</title>
    </head>
    <body>
        <p>Hi there!</p>
        <p>It works!</p>
    </body>
</html>

<!DOCTYPE html>
<html>
    <head>
        <title>Django Girls blog</title>
    </head>
    <body>
        <header>
            <h1><a href="/">Django Girls Blog</a></h1>
        </header>

        <article>
            <time>published: 14.06.2014, 12:14</time>
            <h2><a href="">My first post</a></h2>
            <p>Aenean eu leo quam. Pellentesque ornare sem lacinia quam venenatis vestibulum. Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.</p>
        </article>

        <article>
            <time>published: 14.06.2014, 12:14</time>
            <h2><a href="">My second post</a></h2>
            <p>Aenean eu leo quam. Pellentesque ornare sem lacinia quam venenatis vestibulum. Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut f.</p>
        </article>
    </body>
</html>

# in gitbash
git status
git add .
git status
git commit -m "Changed the HTML for the site."
git push

# in PythonAnywhere command-line
cd ~/jpemberton22.pythonanywhere.com
git pull

# in VSCode Terminal
~/djangogirls$ python manage.py shell
Post.objects.all()
from blog.models import Post
Post.objects.all()
Post.objects.create(author=me, title='Sample title', text='Test')
from django.contrib.auth.models import User
User.objects.all()
me = User.objects.get(username='Jarod')
Post.objects.create(author=me, title='Sample title', text='Test')
Post.objects.all()
Post.objects.filter(author=me)
Post.objects.filter(title__contains='title')
from django.utils import timezone
Post.objects.filter(published_date__lte=timezone.now())
post = Post.objects.get(title="Sample title")
post.publish()
Post.objects.filter(published_date__lte=timezone.now())
Post.objects.order_by('created_date')
Post.objects.order_by('-created_date')
Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
exit()
