from github import Github
import opsutils
from datetime import datetime
# Models for beautiful prints
import sys
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format


# https://github.com/pagarme/pagarme-core/issues/488

#####################
#   CONFIGURATIONS  #
#####################

status_colors = {

    "open": "green",
    "closed": "red",
    "merged": "purple",
    "declined": "blue"
}

organization_name = "pagarme"
repository_name = "pagarme-core"
repository_path = f"{organization_name}/{repository_name}"

issue_number_list = [655, 599, 597, 488, 939]

# strip colors if stdout is redirected
init(strip=not sys.stdout.isatty())

text = "Issues"
cprint(figlet_format(text, font='banner3'), 'green', 'on_blue', attrs=['bold'])

access_info = opsutils.load_access_information(look_at="home")
github_token = access_info["github"]["token"]

access_info = opsutils.load_access_information(look_at="home")
slack_token = access_info["slack"]["token"]

Slack = opsutils.Slack(slack_token)

channel_name = "ops-issues"
filename = "last_update.txt"

update_handler = {}
#####################
#       MAIN        #
#####################

print("Running...")
g = Github(github_token)

repository = g.get_repo(repository_path)

issues = []
for issue_number in issue_number_list:
    issues.append(repository.get_issue(issue_number))


file = open(filename, "r")

for line in file:
    line = line.replace("\n", "")
    line_handler = line.split(",")
    date = datetime.strptime(line_handler[1], "%Y-%m-%d %H:%M:%S")
    update_handler[line_handler[0]] = date

print(update_handler)

for issue in issues:

    issue_number_message = f"issue #{issue.number}"
    issue_status_message = f"status: {issue.state}"

    comments = issue.get_comments()

    comment_slack_message = ""
    for comment in comments:
        comment_message = f"{comment.user.name}: {comment.body} \
({comment.created_at})"

        comment_slack_message = f"{comment_slack_message}\n{comment_message}"

    body_message = f"{issue_status_message}\n\ncomments:\n\
{comment_slack_message}"

    print(f"Sending {issue_number_message} to #{channel_name}...")

    message = f"issue: {issue_number_message}\nmessage:{body_message}"
    print(message)

    if issue.updated_at > update_handler[str(issue.number)]:
        print("ATUALIZADO!!!")
        # file.write(f"{issue.number},{issue.updated_at}\n")

    # # Slack.send_formatted_message(channel_name, issue_number_message,
    #                              status_colors[issue.state], body_message)

file.close()
print("Finished")
