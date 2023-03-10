# Make Your Bed In The Morning

## Social media website (Django web framework)

<a href="http://kjs3980.pythonanywhere.com" target="_blank">Website link</a>

<p float="left">
  <img width="400" alt="make your bed in the morning screenshot homepage" src="https://user-images.githubusercontent.com/96529477/224619056-9fa31e50-9f9f-4db6-876d-9a33c737c10b.png">
  <img width="400" alt="make your bed in the morning screenshot my profile page" src="https://user-images.githubusercontent.com/96529477/224619381-d6674133-66b3-4d74-8880-ad1df5641ab5.png">
  <img width="400" alt="make your bed in the morning screenshot detail page" src="https://user-images.githubusercontent.com/96529477/224620125-b97e4abf-6651-46f1-98f1-aab24eb0c4ca.png">
  <img width="400" alt="make your bed in the morning screenshot about page" src="https://user-images.githubusercontent.com/96529477/224620300-8b1bfbf3-8d33-4aba-a00e-df2e4f05a640.png">
</p>

## Objective

### General Objective

- To share goals of changing the world by making our beds

- To encourage people to focus on the small, and daily tasks that build their positive habits

- Inspired by [Admiral William H. McRaven's full speech on Youtube](https://youtu.be/pxBQLFLei70)

### Technical Objective

- To familiarize with Django Web Framework (Back End)

## Key techniques implemented

### User authentication
 
- Used built-in `User` model
    
    ```py
    from django.contrib.auth.models import User
    ```

- Authenticate / Login / Log out

    - `django.contrib.auth.authenticate`

    - `django.contrib.auth.login`

    - `django.contrib.auth.logout`

### User authorization

```py
if request.user.is_authenticated:
    # perform tasks when user is authenticated
return render(request, 'home.html', {})
```

- Examples

    - Unregistered users can't create a post

    - Unregistered users can't like post

    - Unauthorized users can't edit their posts

    - Unauthorized users can't delete comments

### Established different relationships between different models

- An User creating Posts(User <-> Post.user)

    - An User can write as many Posts as he(she) wants and each Post is written by only one User

    - One-to-many relationship between `django.contrib.auth.models.User` and `blog.models.Post.user`


- Users liking Posts (User <-> Post.liked_users)

    - An User can give 'like' to as many Posts as he(she) want and each Post can receive 'like' by as many Users as it wants.

    - Many-to-many relationship between `django.contrib.auth.models.User` and `django.db.models.Post.liked_users`

- A Post having Comments (Post <-> Comment.post)

    - A Post can have as many Comments and each Comment can be on only one Post

    - One-to-many relationship between `blog.models.Post` and `blog.models.Comment.post`

- An User writing Comments (User <-> Comment.user)

    - An User can write as many Comments as he(she) wants and each Comment is written by only one User

    - One-to-many relationship between `django.contrib.auth.models.User` and `blog.models.Comment.user`

### Storing static files

- By default Django does not track the `media` directory because it is intended for user-uploaded files and it is typically not a good idea to upload user-uploaded files on Github

- However, when deploying on Pythonanywhere.com, I had to create a new media directory on their file structure, so I decided to keep only `media` and ignore all subdirectories under `media`


    ```
    $ touch media/.gitkeep
    ```

    This command allows to keep track of `media` directory

    In <em>.gitignore</em>
    
    ```
    /media/images/
    ```

    This code allows to ignore `media/images` and files in there

- Stored user-uploaded files dynamically

    - Set `media/images/<username>/` as the directory for storing user-uploaded files

        - If username `kjs3980` uploaded his photo named `filename_1.png`, it is stored in `media/images/kjs3980/filename_1.png`

        - If username `randomuser1` uploaded her photo named `randomfile_2.png`, it is stored in `media/images/randomuser1/randomfile_2.png`

    - views.py

        ```py
        # set file path for images in general, and each user's images
        image_folder = os.path.join(os.path.join(settings.MEDIA_ROOT,'images'))
        each_user_folder_path=os.path.join(settings.MEDIA_ROOT, 'images', user.username)

        # if user specific directory doesn't exist
        if not os.path.exists(each_user_folder_path):

            # if image folder doesn't exist
            if not os.path.exists(image_folder):
                os.mkdir(image_folder)

            # dynamically create a directory for each user's images 
            os.mkdir(each_user_folder_path)
        ```

### Send emails

- Set email host as Gmail's SMTP server

    - Two way verification is required.

        Google Account -> Security -> 2-Step Verification (Activate) -> Set App Passwords (App Passwords must be confidential)
    
    - Gmail's SMTP server uses port `587`

- Similar to secret_key, email password key is made sure it is private, not public on Github.

    ```py
    with open(os.path.join(BASE_DIR, 'mysite', 'email_host_password.txt')) as e:
        EMAIL_HOST_PASSWORD = e.read().strip()
    ```

    <em>email_host_password.txt (Example)</em>

    ```
    abcdefghijklmnop
    ```

    No quotation marks around the password

- Used default Django backend for sending emails

    ```py
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    ``` 

- Enabled encrypted message in the email (Transport Layer Security)

    ```py
    EMAIL_USE_TLS = True
    ```

### CRUD

- Create
    
    - Posting, Commenting

- Read

    - Retrieving objects from database (Queryset)

- Update

    - Editing post, personal info

- Delete

    - Deleting post's photo

    - Deleting comment

    - Deleting user

## More updates to add

- Users private messaging

- Keyword tags in posts

- Retweeting(sharing) posts

- Replying to comment

- Follower / Following list

- Suggesting users

- ~~Uploading images~~

- ~~Users deleting their own accounts~~

- ~~Deploying a website~~

- ~~Sending emails~~

- Allowing users to download files

- Unit tests to ensure code quality and functionality
