from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .models import Post, Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

users = User.objects.all()
posts = Post.objects.all()

def home(request):
    users = User.objects.all()
    posts = Post.objects.all().order_by('-created_date')
    like_status = False
    for post in posts:
        if post.likes.filter(pk=request.user.pk).exists():
            like_status = True
    return render(request, 'home.html', {'users':users, 'posts':posts,'like_status':like_status})

def login_view(request):
    users = User.objects.all()
    posts = Post.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        # when signup button is clicked
        if 'signupuser' in request.POST:
            if request.POST['username']:
                user = User.objects.create_user(username=request.POST.get('username'), password=request.POST.get('password'))
                user.save()
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    print(f'{user} signed up & authenticated & logged in')
                    
                    return redirect(request.META.get("HTTP_REFERER", "home"), )
                    # return HttpResponseRedirect(reverse('home'))           

        # when login button is clicked
        elif 'loginuser' in request.POST:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print(f"{user} is authenticated & logged in")
                
                # return HttpResponseRedirect(reverse('home'))
                return redirect(request.META.get("HTTP_REFERER", "home"), )
                
        return redirect(request.META.get("HTTP_REFERER", "home"), )    
        # return render(request, 'home.html', {'user':user, 'users':users, 'posts':posts})
    
    if request.method == "GET":
        return render(request, 'home.html', {'user':user, 'users':users, 'posts':posts})

def logout_view(request):
    logout(request)

    return redirect('home')

def detail_view(request,pk):
    post = Post.objects.get(pk=pk)
    comments = post.comment_set.all()
    
    return render(request, 'detail.html', {'post':post, 'comments':comments})

def create_view(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        if request.method == "POST":
            title=request.POST['title']
            body=request.POST['body']
            post = Post(title=title, body=body, user=user)
            post.save()
            return redirect('detail', pk=post.pk)
        return render(request, 'edit.html', {})
    return redirect('home')

def edit_view(request,pk):
    post = Post.objects.get(pk=pk)
    if post.user.pk == request.user.pk:
        if request.method == "POST":
            title = request.POST['title']
            body = request.POST['body']
            post.title = title
            post.body = body
            post.save()
            return render(request, 'detail.html', {'post':post})
        return render(request, "edit.html", {'post':post})
    return render(request, "detail.html", {'post':post,})

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # people who like this post = post.likes.all()
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user.pk)
        like_status = True
        # if that user already liked the post, then mark user
        
    else:
        post.likes.add(request.user.pk)
        like_status = False
    post.save()
    context = {'like_status':like_status}
    
    return redirect(request.META.get("HTTP_REFERER", "home"), context)
        
def profile_view(request, pk):
    user = User.objects.get(pk=pk)
    posts = Post.objects.filter(user=user)

    return render(request, 'profile.html' , {'user':user, 'posts':posts})

def authenticate_view(request, pk):
    if request.method == "POST":
        password = request.POST.get('password', None)
        
        if password is None:
            messages.error(request, 'Password is required.')
            return redirect('authenticate', pk=pk)
            # return render(request, "authenticate.html", {'pk':pk})

        user = authenticate(username=request.user.username, password=password)
        if user is None:
            messages.error(request, 'Incorrect password.')
            return redirect('authenticate', pk=pk)
        
        return redirect('profile_edit', pk=user.pk)
        
    return render(request, 'authenticate.html', {'pk': pk})

def profile_edit_view(request, pk):

    user = get_object_or_404(User, pk=request.user.pk)
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # print(f"username :{username}, email:{email},password:{password}")
        user_list = list(User.objects.all().exclude(username=request.user.username).values_list('username',flat=True))
        if 'validate-username' in request.POST:
            
            if username not in user_list:
                user.username = username
                
                messages.success(request, f"Username {username} is valid")
                print("valid")
                # return render(request, 'profile_edit.html', {'pk':request.user.pk, 'username':user.username, })
            elif username == user.username:
                
                pass
            else:
                messages.error(request,f"Username {username} is NOT valid")
                print("invalid")
                return redirect('profile_edit',pk=user.pk )

        if 'save' in request.POST:
            #if username is NOT valid
            if username in user_list or not password:
                return redirect('profile_edit', pk=user.pk)
            else:
                user.username = username
                user.set_password(password)
                user.email = email
            user.save()
            login(request, user)
            
            return redirect("profile", pk=user.pk)
    return render(request, 'profile_edit.html', {'pk':request.user.pk, 'username':user.username, })

def comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method =="POST":
        if request.user.is_authenticated:
            new_comment_body = request.POST['body']
            new_comment = Comment(user=request.user, post = post, body=new_comment_body)
            new_comment.save()
        return redirect('detail',pk=pk)
    
    return render(request, "detail.html",{"pk":pk})

def delete_comment(request, pk_post, pk_comment):
    comment = Comment.objects.get(pk=pk_comment)
    if request.user.pk == comment.user.pk and request.user.is_authenticated:
        comment.delete()
    return redirect('detail', pk=pk_post)
