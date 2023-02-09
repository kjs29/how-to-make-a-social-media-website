# A social media website using Django Web Framework

## Objective

- To share goals of changing the world by making our beds

- To encourage people to focus on the small, and daily tasks that build their positive habits

- Inspired by [Admiral William H. McRaven's full speech on Youtube](https://youtu.be/pxBQLFLei70)

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
        
        User can like any post and any post can be liked by many users. 

- CRUD

    - Create
        
        - Posting, Commenting

    - Read

        - Retrieving objects from database

    - Update

        - Editing post, personal info
    
    - Delete

        - Deleting comment

## More updates to add

- Users private messaging

- Keyword tags in posts

- Retweeting(sharing) posts

- Replying to comment

- Following

- Suggesting users

- Uploading images

- Users deleting their own accounts

- Deploying a website