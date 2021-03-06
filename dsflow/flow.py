"""
Usage:
    flow <command> [options]
    flow <command> [options] <value>

Options:
    -m MESSAGE      Command message
    --amend         Commit with amend
    -f              Force push
    -r              Rebase before commiting
    -a              Make git add . before commiting
    -b BRANCH       Specify base, where to send pull request. Default: master

List of availible commands:
    commit           Add file contents to the index
    push             Update remote refs along with associated objects
    pull_request     Send pull request to github
    change           Go to other branch. Start working on new task
    finish           Finish current task
    reset            Reset current branch. Update with last upstream changes


"""
import os
from utils import ALIAS
from fabric.api import local, settings, hide
from settings import GIT_ADD_FIRST, GIT_REBASE_FIRST


PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))


def get_fab_args(command_name, arguments, command_value):
    final_args = []

    if GIT_ADD_FIRST and command_name in ['commit', 'finish']:
        arguments['-a'] = True

    if GIT_REBASE_FIRST and command_name in ['finish', 'push']:
        arguments['-r'] = True

    for key, value in arguments.iteritems():
        if value:
            value = '"%s"' % value.replace(",", "\,") if isinstance(value, str) else value
            final_args.append("%s=%s" % (ALIAS.get(key, key), value))

    if command_value is not None:
        final_args.insert(0, command_value)

    return ",".join(final_args)


def run_command(arguments):
    command_name = arguments.pop('<command>')
    value = arguments.pop("<value>", None)

    command = "fab -f %s/tasks.py %s" % (PROJECT_PATH, command_name)

    additional_args = get_fab_args(command_name, arguments, value)
    if additional_args:
        command += ":%s" % additional_args

    with settings(hide('running'), warn_only=True):
        local(command)


def main():
    from docopt import docopt
    arguments = docopt(__doc__, version='Workflow helper 0.0.1')
    run_command(arguments)
