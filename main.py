""" main.py - Google App Engine flask app and its functions """

# Import wraps for decorators
from functools import wraps

# Import utils
from utils import logger
from utils import valid_username, valid_email, valid_password
from utils import check_secure_value, make_secure_value, compare_authors
from utils import SECRET

# Import datastore models
from models import BlogEntry, Author, Comment

# Import and set up flask
from flask import Flask, g
from flask import render_template, request, redirect, url_for
from flask import flash, get_flashed_messages

app = Flask(__name__)
app.secret_key = SECRET
app.jinja_env.globals.update(compare_authors=compare_authors)


def logged_in(func):
    """ Decorator to check if author is logged in """
    @wraps(func)
    def login_status(*args, **kwargs):
        """ Checks if author is logged in """
        logger.debug("Checking author log in status")

        g.logged_in = False
        g.author_id = None
        cookie = request.cookies.get("author")
        if cookie:
            author_id = check_secure_value(cookie)
            if author_id:
                g.logged_in = True
                g.author_id = long(author_id)

        return func(*args, **kwargs)

    return login_status


@app.route("/")
@logged_in
def index():
    """ The multi-user blog's main page showing all entries """
    logger.debug("============ Main page ============")
    query = BlogEntry.query().order(-BlogEntry.last_modified)
    entries = query.fetch(limit=10)

    return render_template("index.html", entries=entries, logged_in=g.logged_in)


@app.route("/entry/<int:entry_id>", methods=['GET', 'POST'])
@logged_in
def entry(entry_id):
    """ The multi-user blog's page showing a single entry """
    logger.debug("============ Entry page ============")
    entry = BlogEntry.get_by_id(entry_id)

    # Check if author is logged in if they are,
    # allow liking the post, if the post is not theirs
    # and they haven't like it yet.
    # Also allow creation of comment, if user is logged in.
    can_like = False
    if g.author_id:
        logger.debug(g.author_id)
        author_key = Author.get_by_id(g.author_id).key
        if not entry.author.id() == g.author_id and author_key not in entry.likers:
            can_like = True

        if request.method == 'POST':
            comment = Comment.create_comment(
                comment=request.form['comment'],
                author_key=author_key,
                entry_key=entry.key)
            comment.put()

    comments = Comment.query(
        ancestor=entry.key).order(-Comment.last_modified).fetch()

    return render_template("entry.html",
                           can_like=can_like,
                           entry=entry,
                           comments=comments)

@app.route("/entry/<int:entry_id>/like")
@logged_in
def like_entry(entry_id):
    """ Allows logged-in authors to like a post """
    logger.debug("============ Like entry ============")
    if not g.logged_in:
        return redirect(url_for('index'))

    entry = BlogEntry.get_by_id(entry_id)
    if entry.author.id() == g.author_id:
        return redirect(url_for('entry', entry_id=entry.key.id()))

    if g.author_id not in entry.likers:
        entry.likers.append(Author.get_by_id(g.author_id).key)
        entry.put()

    return redirect(url_for('entry', entry_id=entry.key.id()))



@app.route("/entry/new", methods=['GET', 'POST'])
@logged_in
def create_entry():
    """ Allows logged-in author to create blog posts """
    logger.debug("============ Create entry ============")
    if not g.logged_in:
        return redirect(url_for('index'))

    if request.method == 'POST':
        author = Author.get_by_id(g.author_id)
        entry = BlogEntry.create_entry(
            title=request.form['title'],
            body=request.form['body'],
            author_key=author.key)
        entry.put()

        return redirect(url_for("entry", entry_id=entry.key.id()))

    return render_template("create_entry.html")


@app.route("/entry/<int:entry_id>/edit", methods=['POST', 'GET'])
@logged_in
def edit_entry(entry_id):
    """ Allows logged-in author to edit their blog posts """
    logger.debug("============ Edit entry ============")
    if not g.logged_in:
        return redirect(url_for('index'))

    entry = BlogEntry.get_by_id(entry_id)
    if not entry.author.id() == g.author_id:
        return redirect(url_for('index'))

    if request.method == 'POST':
        entry.title = request.form['title']
        entry.body = request.form['body']
        entry.put()

        return redirect(url_for('entry', entry_id=entry_id))

    return render_template("edit_entry.html", entry=entry)


@app.route("/entry/<int:entry_id>/delete", methods=['POST', 'GET'])
@logged_in
def delete_entry(entry_id):
    """ Allows logged-in author to delete their blog posts """
    if not g.logged_in:
        return redirect(url_for('index'))

    entry = BlogEntry.get_by_id(entry_id)
    if not entry.author.id() == g.author_id:
        return redirect(url_for('index'))

    if request.method == 'POST':
        entry.key.delete()
        return redirect(url_for('index'))

    return render_template("delete_entry.html", entry=entry)


@app.route("/entry/<int:entry_id>/comment/<int:comment_id>/edit",
           methods=['GET', 'POST'])
@logged_in
def edit_comment(entry_id, comment_id):
    """ Allows logged-in author to edit their comments """
    logger.debug("============ Edit comment ============")
    if not g.logged_in:
        return redirect(url_for('index'))

    entry = BlogEntry.get_by_id(entry_id)
    comment = Comment.get_by_id(comment_id, parent=entry.key)
    if not comment.author.id() == g.author_id:
        return redirect(url_for('index'))

    if request.method == 'POST':
        comment.comment = request.form['comment']
        comment.put()
        return redirect(url_for('entry', entry_id=entry_id))

    return render_template("edit_comment.html", comment=comment)


@app.route("/entry/<int:entry_id>/comment/<int:comment_id>/delete",
           methods=['GET', 'POST'])
@logged_in
def delete_comment(entry_id, comment_id):
    """ Allows logged-in author to delete their comments """
    if not g.logged_in:
        return redirect(url_for('index'))

    entry = BlogEntry.get_by_id(entry_id)
    comment = Comment.get_by_id(comment_id, parent=entry.key)
    if not comment.author.id() == g.author_id:
        return redirect(url_for('index'))

    if request.method == 'POST':
        comment.key.delete()
        return redirect(url_for('entry', entry_id=entry_id))

    return render_template("delete_comment.html")


@app.route("/logout")
@logged_in
def logout():
    """ Allows authors to log out """
    response = redirect(url_for("index"))

    if g.logged_in:
        response.set_cookie('author', "", expires=0)

    return response


@app.route("/login", methods=['GET', 'POST'])
@logged_in
def login():
    """ Allows registered authors to sign in """
    logger.debug("============ Login ============")
    if g.logged_in:
        return redirect(url_for('index'))

    if request.method == 'POST':
        credentials = (request.form['username'], request.form['password'])

        author = Author.login(credentials)

        if author:
            response = redirect(url_for("index"))
            response.set_cookie("author", make_secure_value(author.key.id()))

            return response

        else:
            flash("Username or password incorrect. Please try again.")

    return render_template("login.html")


@app.route("/signup", methods=['GET', 'POST'])
@logged_in
def signup():
    """ Allows authors to sign up for the blog """
    logger.debug("============ Signup ============")
    if g.logged_in:
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Validate the form fields
        user_name = request.form['username']
        if not valid_username(user_name):
            logger.debug("Username not valid.")
            flash("Invalid username.")

        email_address = request.form['email']
        if not valid_email(email_address):
            logger.debug("Email address not valid.")
            flash("Invalid email address.")

        password = request.form['password']
        if not valid_password(password):
            logger.debug("Password not valid.")
            flash("Invalid password.")

        if not request.form['password'] == request.form['verify']:
            logger.debug("Passwords don't match.")
            flash("Your verification password did not match your password.")

        # Deliver form validation errors, if any
        if get_flashed_messages():
            return render_template("signup.html")


        # Check for username and email address conflicts
        if Author.query(Author.user_name == user_name).get():
            flash("An author with that name already exists.")

        if Author.query(Author.email_address == email_address).get():
            flash("An author with that email address already exists.")

        # Deliver conflicts, if any
        if get_flashed_messages():
            return render_template("signup.html")


        # Create new author
        author = Author.signup(
            name=request.form['username'],
            password=password,
            email=request.form['email'])
        author.put()

        response = redirect(url_for('index'))
        response.set_cookie("author", make_secure_value(author.key.id()))

        return response

    return render_template("signup.html")
