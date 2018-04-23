import opsutils

access_info = opsutils.load_access_information(look_at="home")
slack_token = access_info["slack"]["token"]

Slack = opsutils.Slack(slack_token)
# Slack.send_message("ops-issues", "Olaaa")

Slack.send_formatted_message("ops-issues", "titulo", "green", "\ntextaaao")
