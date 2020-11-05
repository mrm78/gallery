from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from orders.models import product, session
from home.models import article, article_comment

def home(req):
    return render(req, 'index.html', {'products':product.objects.all(), 'articles':article.objects.all()})


def Article(req, ID):
    a = article.objects.get(id=ID)
    a.view_counter += 1
    a.save()
    return render(req, 'article.html', {'articles':article.objects.all(), 'article':a})


def list_articles(req):
    return render(req, 'list-articles.html', {'articles':article.objects.all()})

#adding a new product to server by adm
@login_required
def add_product(req):
    if not req.user.is_superuser:
        return 0
    if req.method == 'GET':
        return render(req, 'add-product.html')
    name = req.POST['name']
    summary = req.POST['summary']
    f = req.FILES['file']
    image = req.FILES['image']
    videos_number = req.POST['videos_number']
    presentor = req.POST['presentor']
    price = int(req.POST['price'])
    time = req.POST['time']
    off = int(req.POST['off']) / 100
    p = product(File=f,image=image, summary=summary.encode(), name=name.encode(), videos_number=videos_number.encode(), presentor=presentor.encode(), price=price, off=off, time=time.encode())
    p.save()
    for i in range(1,11):
        if req.POST[f'topic{i}']:
            s = session(product=p, topic=req.POST[f'topic{i}'].encode(), number=i, time=req.POST[f'time{i}'].encode())
            s.save()
    return redirect('home')

@login_required
def edit_product(req, ID):
    if not req.user.is_superuser:
        return 0
    p = product.objects.get(id=ID)
    if req.method == 'GET':
        return render(req, 'edit-product.html', {'product':p})
    p.name = req.POST['name'].encode()
    p.summary = req.POST['summary'].encode()
    p.videos_number = req.POST['videos_number']
    p.presentor = req.POST['presentor'].encode()
    p.price = int(req.POST['price'])
    p.time = req.POST['time'].encode()
    p.off = int(req.POST['off']) / 100
    if req.FILES.get('file'):
        p.File = req.FILES['file']
    if req.FILES.get('image'):
        p.image = req.FILES.get('image')
    p.save()
    p.session_set.all().delete()
    for i in range(1,11):
        if req.POST.get(f'topic{i}'):
            s = session(product=p, topic=req.POST[f'topic{i}'].encode(), number=i, time=req.POST[f'time{i}'].encode())
            s.save()
    return redirect('home')


#adding a new article to server by admin
@login_required
def add_article(req):
    if not req.user.is_superuser:
        return 0
    if req.method == 'GET':
        return render(req, 'add-article.html')
    topic = req.POST['topic']
    text = req.POST['text']
    image = req.FILES['image']
    presentor = req.POST['presentor']
    a = article(text=text.encode(), image=image, topic=topic.encode(), presentor=presentor.encode())
    a.save()
    return redirect('home')

@login_required
def edit_article(req, ID):
    if not req.user.is_superuser:
        return 0
    a = article.objects.get(id=ID)
    if req.method == 'GET':
        return render(req, 'edit-article.html', {'article':a})
    a.topic = req.POST['topic'].encode()
    a.text = req.POST['text'].encode()
    a.presentor = req.POST['presentor'].encode()
    if req.FILES.get('image'):
        a.image = req.FILES.get('image')
    a.save()
    return redirect('home')


@login_required(login_url='login')
def article_commenting(req):
    if req.method == "POST":
        text = req.POST['text']
        a = article.objects.get(id=int(req.POST['article_id']))
        c = article_comment(article=a, user=req.user, text=text.encode())
        c.save()
        return redirect('article', ID=a.id)