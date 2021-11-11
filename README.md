# TheBestBlog
TheBestBlog by Team The Best Cameron
<br>
Cameron Nelson - Python/SQLite3/Backend
Alif Abdullah - Python/SQLite3/Backend
Kevin Cao - HTML/Jinja/CSS Frontend
Jonathan Wu - HTML/Jinja/CSS Frontend

## About

TheBestBlog is a blog hosting site. Signed up & logged in users can create blogs, update their blogs by adding new entries, and edit existing entries for their blogs.
Non-logged in users can view all blogs, a specific blog, or a random blog.

## Install Instructions:

Run the following commands in a terminal shell with git and python installed:

`git clone git@github.com:cnelson20/TheBestBlog.git`

`cd TheBestBlog/app/`

`python3 -m venv ~/blogenv`

Wait until that process finishes, then run:

`source ~/blogenv/bin/activate `

If you use windows, you may have to run source `~/blogenv/scripts/activate` instead

If that works, your terminal should appear something like this: <br>
`(blogenv) ~/TheBestBlog/app/`

If that's correct, run <br>
`pip install -r ../requirements.txt`

Wait for that to complete, and then

`python3 app.py` and the webserver should start up and start serving pages.
