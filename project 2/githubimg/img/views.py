import email
import profile
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
from bs4 import BeautifulSoup as bs
from .models import Github



# Create your views here.
# session = requests.Session()
# retry = Retry(connect=3, backoff_factor=0.5)
# adapter = HTTPAdapter(max_retries=retry)
# session.mount('http://', adapter)
# session.mount('https://', adapter)
# #
def index(request):
    if request.method =='POST':
        github_user = request.POST['github_user']
        user = request.POST['user']
        url ='https://github.com/'+github_user
        r =requests.get(url)
        soup =bs(r.content)
        profile = soup.find('img',{'alt': 'Avatar'})['src']
        #print(profile)
        new_github = Github(
            githubuseer = github_user,
            imagelink = profile,
            username = user
        )
        new_github.save()
        messages.info(request, 'User '+ github_user +' Image Saved')
        return redirect('/')
        
        

    return render(request,'index.html')

def register(request):
    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'username Taken')
                return redirect('register')
            else:
                user =User.objects.create_user(username=username, email=email, password =password)
                user.save(); #save the user to the database.
                return redirect('login')
        else:
            messages.info(request,'password not matching')
            return redirect('/')
    else:
        return render(request,'signup.html')   



def login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid credentials')  
            return redirect('login')  



    else:
         return render(request,'login.html') #Reverse for '<WSGIRequest: happen because you used redirect instead of render 


def logout(request):
    auth.logout(request)
    return redirect('login') 

def images(request):
    username = request.user
    git_hub =Github.objects.filter(username = username)
    return render(request,"images.html", {'git_hub':git_hub})        