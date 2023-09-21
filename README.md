# Readit API

Readit is a simple social media API that allows users to post text content, interact with posts, and manage their accounts. This README.md file serves as a guide to get you started with the Readit API.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Creating an Account](#creating-an-account)
  - [Logging In](#logging-in)
  - [Post Operations](#post-operations)
  - [Interacting with Posts](#interacting-with-posts)
  - [Account Deletion](#account-deletion)

## Features

- User authentication
- Post creation, reading, updating, and deletion
- User interactions with posts (like, upvote, downvote, comment)


## Requirements

Before you can run the Readit API, make sure you have the following installed:

- Python (version 3.7 or higher)
- Flask (install via `pip install Flask`)
- Other dependencies (install via `pip install -r requirements.txt`)
- Postgres Database

## Installation

1. Clone the Readit API repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/readit-api.git
   cd readit-api
   ```
2. Create a virtual environment (recommended)

   ```bash
    python -m venv venv
    source venv/bin/activate
   ```
3. Install the required dependencies
    ```
    pip install -r requirements.txt
    ```
4. Run the Application

## Usage
### Creating an Account

To create a new user account, make a POST request to the `/signup` endpoint with the following JSON data:

    {
        "username": "your_username",
        "email": "your_email",
        "password": "your_password"
        "password2": "confirm_your_password",
        "age": "your_age",
        "gender": "your_gender"
    }
    
### Logging in

To log in to your account, make a POST request to the `/login` endpoint with your credentials:

    {
        "email": "your_email",
        "password": "your_password"
    }

#### Note: For all of the below endpoints, the user needs to be authenticated and have a JWT token in  the header of each request

### Logging Out
To log out of your account, make a GET request to `/logout` endpoint

### Account Deletion
Make a Delete request to `/account/delete` endpoint

### Getting Profile
Make a GET request to  `/profile` endpoint

### Post Operations

#### Creating Post
Create a Post: Make a POST request to `/post/create` with the following JSON data:

    {
        "title": "Your Post Title",
        "content": "Your post content goes here"
    }
#### Get all posts
Make a GET request to `/home?page=1` to retrieve latest `10` posts. To get `next 10` change the `page` query parameter

#### Update a Post
Make a PUT request to `/post/update?pid=1` with the updated post data. Here `pid` is `post id`, So, put the id of the post that you want to update

#### Delete a Post
Make a DELETE request to `/post/delete?pid=1` to delete a post. Here `pid` is `post id`, So, put the id of the post that you want to delete

#### Get Votes on Post
Make a GET request to `/post/votes?post_id=1`. Use the `post_id` of the post, whose votes you want to get

#### Get Comments on a Post
Make a GET request to `/post/comments?post_id=1&page=1`. Use the `post id` of the Post, whose comments you want to get. `page` = 1 gives the latest 30 comments on a Post, to get more Comments change the value to 2 and so on

### Interacting with Posts
#### Voting on a Post
Make a GET request TO `/vote?pid=1&value=1` endpoint. Here `pid` is `post id` and value tells whether it's an `upvote` or `downvote` (use 1 for upvote and -1  for downvote)

#### Deleting Vote
Make a DELETE request to `/vote/delete/pid=1`. Here `pid` is `post id`. So, put the id of the Post from which you want to delete your vote

#### Comment on a Post
Make a POST request to `/comment/create/pid=1` endpoint with the following JSON data:

    {
        "content": "Your Comment goes here"
    }
Here `pid` refers to `post id`. So, use the value of `pid` accordingly

#### Deleting Comment
Make a DELETE request to `/comment/delete?comment_id=1` endpoint. Use the `comment id` of the comment that you want to delete

