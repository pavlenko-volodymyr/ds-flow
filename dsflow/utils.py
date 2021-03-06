from functools import wraps, partial

from fabric.api import local, quiet
from requests import post

from settings import GITHUB, PULL_REQUEST_MSG_PREFIX

ALIAS = {
    '-f': 'force',
    '-m': 'message',
    '--amend': 'amend',
    '-r': 'need_rebase',
    '-a': 'add_first',
    '-b': 'base'
}

post = partial(post, auth=(GITHUB['user'], GITHUB['password']))


def memoize(func):

    cache = {}

    @wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap


@memoize
def get_branch_name():
    with quiet():
        return local("git rev-parse --abbrev-ref HEAD", capture=True)


def get_commit_message(message=None, branch_name=None):
    if not message:
        return get_last_commit_message()
    else:
        branch_name = branch_name or get_branch_name()
        return "%s, %s" % (branch_name.capitalize(), message)


def get_last_commit_message():
    with quiet():
        return local("git log -1 --pretty=%B", capture=True)
