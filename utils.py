"""utils.py - contains various utility functions """

import re
import random
import hashlib
import hmac
from string import letters

# Logger adapted from the python docs
import logging
# Create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)
# Create console handler
ch = logging.StreamHandler()
# Set logging level
ch.setLevel(logging.DEBUG)
# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Add formatter to console handler
ch.setFormatter(formatter)
# Add console handler to logger
logger.addHandler(ch)


# app secret
SECRET = "[your-secret]"


# The following functions and regexes have been mostly taken off the course material
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    """ Check if a username is valid """
    return username and USER_RE.match(username)


PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    """ Check if a passowrd is valid """
    return password and PASS_RE.match(password)


EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    """ Check if a email address is valid """
    return not email or EMAIL_RE.match(email)


def compare_authors(authors, compare_with):
    """ Compares two author id to see if they are identical """
    return authors.id() == compare_with


def check_secure_value(secure_value):
    """ Takes a secure value and checks if it was not tampered with """
    value = secure_value.split('|')[0]
    if secure_value == make_secure_value(value):
        return value


def generate_pw_hash(name, password, salt=None):
    """ Returns a hashed password """
    if not salt:
        salt = generate_salt()

    hash_pw = hashlib.sha256(name + password + salt).hexdigest()
    return "%s,%s" % (salt, hash_pw)


def generate_salt(length=5):
    """ Returns a random salt """
    return ''.join(random.choice(letters) for x in xrange(length))


def check_pw(name, password, pw_hash):
    """ Validate a password with its hash """
    salt = pw_hash.split(',')[0]
    return pw_hash == generate_pw_hash(name, password, salt)


def make_secure_value(value):
    """ Return a tuple of a value and secret representation """
    value = str(value)
    return '%s|%s' % (value, hmac.new(SECRET, value).hexdigest())
