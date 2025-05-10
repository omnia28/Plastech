from django.shortcuts import render, redirect
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ContactForm

# Create your views here.
def home(request):
    articles = fetch_water_pollution_articles()[1:4]
    return render(request, 'pages/home.html', {"articles": articles})

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})

def fetch_water_pollution_articles():
    url = f"https://newsapi.org/v2/everything?q=microplastic&apiKey=bb9946e024434e8db8c71615d0368f32"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("articles", [])
    return []

def article_list(request):
    articles = fetch_water_pollution_articles()
    page = request.GET.get('page')
    paginator = Paginator(articles, 9) 

    try:
        articles_page = paginator.page(page)
    except PageNotAnInteger:
        articles_page = paginator.page(1)
    except EmptyPage:
        articles_page = paginator.page(paginator.num_pages)

    return render(request, "pages/blogs.html", {"articles": articles_page})