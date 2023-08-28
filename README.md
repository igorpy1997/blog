# blog
Deploying version: http://igorpy.pythonanywhere.com/main/

A pet project for creating a blog using the Django framework and JavaScript.
- Users can register, log in, and log out.
- Users can create posts (login required).
- Users can publish posts or save them as drafts (users can later publish them).
- Users can edit their posts (login required, filter(owner=...)).
- Anonymous users can post comments.
- Comments are moderated before being published (is_published field + admin page).
- Administrators receive email notifications about new posts or comments (console).
- Users receive notifications about new comments on their posts with a link to the post (console) (start with sending an email on comment creation).
- There is a page with a list of all posts.
- There is a page with a list of a user's posts.
- There is a post detail page.
- There is a public profile page.
- There is a profile page where users can edit their information.
- Pagination for posts and comments.
- Posts have a title, short description, image (optional link to image or actual image file), and full description.
- Comments have a username and text (just two text fields).
- Lorem ipsum fixtures.
- Admin panel with functionality.
- Contact form for communication with the admin (console).
- Stylish templates.
- Different settings for development and production.
- Query optimization.
- Caching.
- Celery.
- Deploy to PythonAnywhere, Heroku, DigitalOcean, or any other platform for production (without caching and background tasks).
