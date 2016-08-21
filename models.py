""" models.py - Google App Engine datastore models """

# Import utils
from utils import generate_pw_hash, check_pw

# Import Google App Engine moduls
from google.appengine.ext import ndb


# ================ Model definitions ================
# ================ Blog post         ================
class BlogEntry(ndb.Model):
    """ A class to represent blog posts """
    # Basic information
    title = ndb.StringProperty(required=True)
    body = ndb.TextProperty(required=True)
    author = ndb.KeyProperty(required=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)

    # Like information
    likers = ndb.KeyProperty(repeated=True)
    likes = ndb.ComputedProperty(lambda self: len(self.likers))

    def __repr__(self):
        return "BlogEntry(%r, %r, %r. %r, %r, %r)" % (
            self.title,
            self.body,
            self.author,
            self.last_modified,
            self.likers,
            self.likes)

    @classmethod
    def create_entry(cls, title, body, author_key):
        """ Returns a new BlogEntry """
        return BlogEntry(
            title=title,
            body=body,
            author=author_key)


# ================ Comment           ================
class Comment(ndb.Model):
    """ A class to represent comment on blog posts """
    comment = ndb.TextProperty(required=True)
    author = ndb.KeyProperty(required=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)

    def __repr__(self):
        return "Comment(%r, %r, %r)" %(
            self.comment,
            self.author,
            self.last_modified)

    @classmethod
    def create_comment(cls, comment, author_key, entry_key):
        """ Returns a new Comment """
        return Comment(
            comment=comment,
            author=author_key,
            parent=entry_key)


# ================ Author            ================
class Author(ndb.Model):
    """ A class to represtend blog post / comment authors """
    user_name = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    email_address = ndb.StringProperty(required=True)

    def __repr__(self):
        return "Author(%r, %r)" % (self.user_name,
                                   self.email_address)

    @classmethod
    def signup(cls, name, password, email):
        """ Hashes the password and creates a new Author """
        pw_hash = generate_pw_hash(name, password)

        return Author(
            user_name=name,
            password=pw_hash,
            email_address=email)

    @classmethod
    def login(cls, credentials):
        """ Check if login credentials are valid. If yes,
        get and return author from datastore """
        user_name, password = credentials

        author = cls.get_by_name(user_name)
        if author and check_pw(user_name, password, author.password):
            return author

    @classmethod
    def get_by_name(cls, name):
        """ Retrievs an author form the datastore using
        their username """
        author = Author.query(
            Author.user_name == name).get()
        return author
