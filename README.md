# A social media website using Django Web Framework

[Website link](http://kjs3980.pythonanywhere.com)

<img width="360" alt="Screenshot 2023-02-12 at 12 08 37 AM" src="https://user-images.githubusercontent.com/96529477/218298257-be205c61-851c-4b4c-8fbc-33637aff7d67.png">

## Objective

### General Objective

- To share goals of changing the world by making our beds

- To encourage people to focus on the small, and daily tasks that build their positive habits

- Inspired by [Admiral William H. McRaven's full speech on Youtube](https://youtu.be/pxBQLFLei70)

### Technical Objective

- To familiarize with Django Web Framework (Back End)

## Key techniques implemented

- User authentication
 
    - Login / Log out
    
        - Used built-in `User` model
        
            ```py
            from django.contrib.auth.models import User
            ```

- User authorization

    - Unregistered users can't create a post

    - Unregistered users can't like post

    - Unauthorized users can't edit their posts

    - Unauthorized users can't delete comments

- User liking post

    - Many-to-many relationships between `django.contrib.auth.models.User` and `django.db.models.Post.likes`
        
        User can like any post and any post can receive 'like' by any user.

- Send emails

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

- CRUD

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
