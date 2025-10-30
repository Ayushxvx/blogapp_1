from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request,"a/index.html",{"posts":posts})

def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = User.objects.get(email=email).username
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect("index")
        else:
            messages.error(request,"Invalid Credentials")
    
    return render(request,"a/login.html")


def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = request.POST.get("username").lower()
        user = User.objects.filter(username=username)
        if user.exists():
            messages.error(request,"Username already taken!")
        elif User.objects.filter(email=email).exists():
            messages.error(request,"Email already in use!")
        else:
            user = User.objects.create_user(username,email,password)
            messages.success(request,"User created successfully")
    return render(request,"a/signup.html")

@login_required(login_url="login_user")
def logout_user(request):
    logout(request)
    return redirect("index")

@login_required(login_url="login_user")
def add_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        img = request.FILES.get("image")
        vid = request.FILES.get("video")
        print(f"Title = {title}\nDescription={description}\nImg = {img}")
        if img and vid:
            post = Post(title=title,description=description,img=img,vid=vid,author=request.user)
            post.save()
            messages.success(request,"New Post added successfully")
        elif img:
            post = Post(title=title,description=description,img=img,author=request.user)
            post.save()
            messages.success(request,"New Post added successfully")
        elif vid:
            post = Post(title=title,description=description,vid=vid,author=request.user)
            post.save()
            messages.success(request,"New Post added successfully")
        else:
            post = Post(title=title,description=description,author=request.user)
            post.save()
            messages.success(request,"New Post added successfully")

    return render(request,"a/addpost.html")

def post_detail(request,pk=None):
    post = Post.objects.get(id=pk)
    return render(request,"a/postdetail.html",{"post":post})

@login_required(login_url="login_user")
def like_post(request,pk):
    post = Post.objects.get(id=pk)
    like = Like.objects.filter(post=post,author=request.user)
    if like.exists():
        like.delete()
    else:
        like = Like(post=post,author=request.user)
        like.save()
        if Dislike.objects.filter(post=post,author=request.user).exists():
            Dislike.objects.get(post=post,author=request.user).delete()
    return redirect("post_detail",pk=post.id)

@login_required(login_url="login_user")
def dislike_post(request,pk):
    post = Post.objects.get(id=pk)
    dislike = Dislike.objects.filter(post=post,author=request.user)
    if dislike.exists():
        dislike.delete()
    else:
        dislike = Dislike(post=post,author=request.user)
        dislike.save()
        if Like.objects.filter(post=post,author=request.user).exists():
            Like.objects.get(post=post,author=request.user).delete()
    return redirect("post_detail",pk=post.id)

@login_required(login_url="login_user")
def add_comment(request,pk):
    if request.method == "POST":
        post = Post.objects.get(id=pk)
        text = request.POST.get("comment")
        comment = Comment(post=post,author=request.user,text=text)
        comment.save()
    
    return redirect("post_detail",pk=post.id)

@login_required(login_url="login_user")
def del_comment(request,pk,id):
    if request.method == "POST":
       comment = Comment.objects.get(id=id)
       if comment.author == request.user:
           comment.delete()
       else:
           pass
    
    return redirect("post_detail",pk=pk)


@login_required(login_url="login_user")
def profile(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-created_at')
    liked_posts = Post.objects.filter(likes__author=request.user)
    disliked_posts = Post.objects.filter(dislikes__author=request.user)
    commented_posts = Post.objects.filter(comments__author=request.user)
    return render(request,"a/profile.html",{
        'user':user,
        "posts":posts,
        "liked_posts":liked_posts,
        "disliked_posts":disliked_posts,
        "commented_posts":commented_posts,
    })


def del_post(request,id):
    post = Post.objects.get(id=id)
    if post.author == request.user:
        post.delete()
    
    return redirect("profile")

def anything(request,anything):
    return HttpResponse(f"<h1> There's no page as for {anything} :)")