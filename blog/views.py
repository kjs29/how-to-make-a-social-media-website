from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .models import Post, Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
import os, shutil


def home(request):
    """Home page view"""
    users = User.objects.all()
    posts = Post.objects.all().order_by('-created_date')
    like_status = False
    for post in posts:
        if post.likes.filter(pk=request.user.pk).exists():
            like_status = True

    return render(request, 'home.html', {'users':users, 'posts':posts,'like_status':like_status})

def about_view(request):
    return render(request, 'about.html', {})

def contact_view(request):
    if request.method == "POST":
        subject = request.POST['subject']
        body = request.POST['body']
        sender_email = request.POST['email'].lower()
        
        email_to_myself = EmailMessage(
            f"[Django website requests : {subject}]",
            f"""
            Subject : {subject}<br><br>
            
            Body : {body}<br><br>
            
            Requested Email : {sender_email}
            """,
            to=['jsk.jinsung@gmail.com'],
            reply_to=[sender_email]
        )

        email_to_customer = EmailMessage(
            "Thank you for your request",
            f"""
            We have received your message,<br><br>
            
            Your message : <br><strong>{body}</strong><br><br><br>

            If this message is what you wrote, please type 'Confirmed' in the reply.<br><br>
            
            We will get in touch with you as soon as we can.<br><br>

            Thank you.<br><br>
            
            Let's change the world!
            """,
            '"Make Your Bed" <settings.EMAIL_HOST_USER>',
            to=[sender_email],
            
        )
        email_to_myself.content_subtype = 'html'
        email_to_customer.content_subtype = 'html'
        email_to_myself.send()
        email_to_customer.send()

        return redirect('thankyou')
    return render(request, 'contact.html',{})
def thankyou(request):
    return render(request,'thankyou.html',)

def login_view(request):
    """Log in view"""

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        # when signup button is clicked
        if 'signupuser' in request.POST:
            if request.POST['username']:
                user = User.objects.create_user(username=request.POST.get('username'), password=request.POST.get('password'))
                user.save()
                user = authenticate(request, username=username, password=password)
                
                # when an user's credentials are authenticated
                if user is not None:
                    login(request, user)

                    return redirect(request.META.get("HTTP_REFERER", "home"), )
                else:
                    messages.error(request, "Choose different Username or(and) Password")

        # when login button is clicked
        elif 'loginuser' in request.POST:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
    
                return redirect(request.META.get("HTTP_REFERER", "home"), )
            messages.error(request, "Invalid Username or(and) Password") 

        return redirect(request.META.get("HTTP_REFERER", "home"), )
    
    # when request.method == "GET"
    # log in view is in the Navbar, therefore most likely it needs to READ users and posts
    users = User.objects.all()
    posts = Post.objects.all()

    return render(request, 'home.html', {'user':user, 'users':users, 'posts':posts})

def logout_view(request):
    """Log out view"""
    
    logout(request)

    return redirect('home')

def detail_view(request,pk):
    """Post detail view"""

    post = Post.objects.get(pk=pk)
    comments = post.comment_set.all().order_by('-created_date')
    
    return render(request, 'detail.html', {'post':post, 'comments':comments})

def create_view(request):
    """Create post view"""

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        if request.method == "POST":
            title=request.POST['title']
            body=request.POST['body']
            file=request.FILES.get('file')
            image_folder = os.path.join(os.path.join(settings.MEDIA_ROOT,'images'))
            each_user_folder_path=os.path.join(settings.MEDIA_ROOT, 'images', user.username)
            if not os.path.exists(each_user_folder_path):
                if not os.path.exists(image_folder):
                    os.mkdir(image_folder)
                os.mkdir(each_user_folder_path)
            if file:
                with open(os.path.join(each_user_folder_path, title), "wb+") as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                file_path = os.path.join('images', user.username, title)
                post = Post(title=title, body=body, user=user, photo=file_path, original_filename=file.name)
            else:
                post = Post(title=title, body=body, user=user)
            post.save()

            return redirect('detail', pk=post.pk)

        return render(request, 'edit.html', {})

    return redirect(request.META.get("HTTP_REFERER", "home"), )

def edit_view(request,pk):
    """Edit post view"""

    post = get_object_or_404(Post, pk=pk)
    if post.user.pk == request.user.pk:
        if request.method == "POST":
            title = request.POST['title']
            body = request.POST['body']
            file = request.FILES.get('file')
            image_folder = os.path.join(os.path.join(settings.MEDIA_ROOT,'images'))
            each_user_folder_path=os.path.join(settings.MEDIA_ROOT, 'images', post.user.username)
            if not os.path.exists(each_user_folder_path):
                if not os.path.exists(image_folder):
                    os.mkdir(image_folder)
                os.mkdir(each_user_folder_path)
            if file:
                post.photo.delete()
                with open(os.path.join(each_user_folder_path, title), "wb+") as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                file_path = os.path.join('images', post.user.username, title)
                post.photo = file_path
                post.original_filename = file.name
            post.title = title
            post.body = body
            
            post.save()
            
            return redirect('detail', pk=pk)

        original_filename = post.original_filename
        return render(request, "edit.html", {'post':post, 'original_filename':original_filename})

    return render(request, "detail.html", {'post':post,})

def like_post_view(request, pk):
    """Like post view"""

    post = get_object_or_404(Post, pk=pk)
    
    # all people who like this post = post.likes.all()
    if post.likes.filter(pk=request.user.pk).exists():

        # post.likes.remove(request.user) raises LazyObjectError when user is NOT authenticated
        # user's pk is allowed to pass in here, and it doesn't raise error since AnonymousUser's pk is None
        print(f"hello? :{request.user.pk}")
        post.likes.remove(request.user.pk)
        like_status = True
        
    else:
        print(f"hello? :{request.user.pk}")
        post.likes.add(request.user.pk)
        like_status = False
    post.save()
    context = {'like_status':like_status}
    
    return redirect(request.META.get("HTTP_REFERER", "home"), context)
        
def profile_view(request, pk):
    """User profile view"""

    user = User.objects.get(pk=pk)
    posts = Post.objects.filter(user=user)

    return render(request, 'profile.html' , {'user':user, 'posts':posts})

def authenticate_view(request, pk):
    """Authenticate user view"""

    if request.method == "POST":
        password = request.POST.get('password', None)
        
        if password is None:
            messages.error(request, 'Password is required.')

            return redirect('authenticate', pk=pk)

        user = authenticate(username=request.user.username, password=password)
        if user is None:
            messages.error(request, 'Incorrect password.')

            return redirect('authenticate', pk=pk)
        
        return redirect('profile_edit', pk=user.pk)
        
    return render(request, 'authenticate.html', {'pk': pk})

def profile_edit_view(request, pk):
    """Profile edit view"""

    user = get_object_or_404(User, pk=request.user.pk)
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user_list = list(User.objects.all().exclude(username=request.user.username).values_list('username',flat=True))

        # validating user's name, not saving now
        if 'validate-username' in request.POST:
            
            if username not in user_list and username.isalnum():
                user.username = username    
                messages.success(request, f"Username {username} is valid")
            
            # when user input contains special characters
            elif not username.isalnum():
                special_characters = set()
                for each in username:
                    if not each.isalnum():
                        special_characters.add(each)
                special_characters = ", ".join(str(x) for x in special_characters)
                messages.error(request, f"Username can't contain special character(s) < {special_characters} >")

            else:
                messages.error(request,f"Username {username} is NOT valid")
                
                return redirect('profile_edit',pk=user.pk)

        # when save button is clicked
        if 'save' in request.POST:
            
            # when username is valid
            if username not in user_list and username.isalnum():
                
                # password is empty
                if not password:
                    user.username = username
                    user.save()
                
                # password is not empty
                else:
                    user.username = username
                    user.set_password(password)
                    user.email = email
                user.save()
                login(request, user)

                return redirect('profile', pk=user.pk)
            
            # when username is NOT valid
            messages.error(request,f"Username {username} is NOT valid")
            return redirect('profile_edit', pk=user.pk)

    return render(request, 'profile_edit.html', {'pk':request.user.pk, 'username':user.username, })

def comment_view(request, pk):
    """Comment on post view"""

    post = get_object_or_404(Post, pk=pk)
    if request.method =="POST":
        if request.user.is_authenticated:
            new_comment_body = request.POST['body']
            new_comment = Comment(user=request.user, post = post, body=new_comment_body)
            new_comment.save()

        return redirect('detail',pk=pk)
    
    return render(request, "detail.html",{"pk":pk})

def delete_comment_view(request, pk_post, pk_comment):
    """Delete comment view"""

    comment = Comment.objects.get(pk=pk_comment)
    if request.user.pk == comment.user.pk and request.user.is_authenticated:
        comment.delete()
        
    return redirect('detail', pk=pk_post)

def delete_user_view(request, pk):
    """
    Delete user view
    - delete posts, comments, image files uploaded by user
    """

    user = get_object_or_404(User, pk = pk)
    if request.user.pk == user.pk and request.user.is_authenticated:
        user.delete()
        directory = os.path.join(settings.MEDIA_ROOT, 'images')
        if user.username in directory:
            shutil.rmtree(os.path.join(directory, user.username))
    
    return redirect('home', )

def delete_post_view(request, pk):
    """Delete post view"""
    
    post = Post.objects.get(pk=pk)
    if request.user == post.user and request.user.is_authenticated:
        post.photo.delete()
        post.delete()

    return redirect('home', )

def delete_photo_view(request, pk):
    """Delete post photo view"""

    post = get_object_or_404(Post, pk=pk)
    post.photo.delete()

    return redirect('edit', pk=pk)

