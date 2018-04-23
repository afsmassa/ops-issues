from github import Github
import opsutils
# Models for beautiful prints
import sys
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format


# https://github.com/pagarme/pagarme-core/issues/488

#####################
#   CONFIGURATIONS  #
#####################

repository_name = "pagarme-core"
issue_number_list = [655, 599, 597, 488]

# strip colors if stdout is redirected
init(strip=not sys.stdout.isatty())

text = "Git.API"
cprint(figlet_format(text, font='banner3'), 'green', 'on_blue', attrs=['bold'])

access_info = opsutils.load_access_information(look_at="home")
github_token = access_info["github"]["token"]

access_info = opsutils.load_access_information(look_at="home")
slack_token = access_info["slack"]["token"]

Slack = opsutils.Slack(slack_token)

channel_name = "ops-issues"

#####################
#       MAIN        #
#####################

g = Github(github_token)

for repo in g.get_user().get_repos():
    if repo.name == repository_name:
        repository = repo

issues = []
for issue_number in issue_number_list:
    issues.append(repository.get_issue(issue_number))

for issue in issues:
    issue_message = f"\nissue #{issue.number}: {issue.state}"

    print(issue_message)
    Slack.send_message(channel_name, issue_message)

    comments = issue.get_comments()

    print("comments:\n")
    Slack.send_message(channel_name, "comments:\n")

    for comment in comments:
        comment_message = f"\t{comment.user.name}: {comment.body} \
({comment.created_at})"
        print(comment_message)
        comment_slack_message = f"```{comment_message}```"
        Slack.send_message(channel_name, comment_slack_message)
