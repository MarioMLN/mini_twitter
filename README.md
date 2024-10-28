# Django REST API

This is a repository for a REST API developed with Django and the Django REST Framework. This document contains instructions for setting up the environment, including Docker, database and running tests local and in GitHub Actions.
---

## Requirements

Install Docker: https://docs.docker.com/engine/install/
and Sign up on Docker Hub: https://hub.docker.com/

Choose a folder in your pc and clone this repository:
```bash
git clone https://github.com/MarioMLN/mini_twitter.git
cd mini_twitter
```

To start the virtual environment:
```bash
source venv/Scripts/activate
```

Docker needs to install all required libraries and start containers:
```bash
docker-compose up --build -d
```
Using Docker-compose, you need to make all initial migrations:
```bash
docker-compose run --rm app sh -c "python manage.py makemigrations"
docker-compose run --rm app sh -c "python manage.py migrate"
```
To start the conection with the linked services:
```bash
docker-compose up -d
```
Other way to run the server is:
```bash
docker-compose run --rm app sh -c "python manage.py runserver"
```
## Tests
User Registration Test Case
```bash
docker-compose run --rm app sh -c "python manage.py test user.tests.test_user_app.UserRegistrationTestCase"
```
User Login Test Case
```bash
docker-compose run --rm app sh -c "python manage.py test user.tests.test_user_app.UserLoginTestCase"
```
Follow and Unfollow Test Case
```bash
docker-compose run --rm app sh -c "python manage.py test user.tests.test_user_app.FollowUnfollowTestCase"
```
Post Test Case - Create, Update, Delete and Get
```bash
docker-compose run --rm app sh -c "python manage.py test feed.tests.test_feed_app.PostTestCase"
```
User Feed Test Case
```bash
docker-compose run --rm app sh -c "python manage.py test feed.tests.test_feed_app.UserFeedTestCase"
```
Like View Test Case
```bash
docker-compose run --rm app sh -c "python manage.py test feed.tests.test_feed_app.LikeViewTestCase"
```
