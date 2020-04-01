# BotJira
This is a bot that collects information from some Jira project and sends it to google chat using webhook.
 
The bot collects information from the Jira API and notifies the chat with some information:

The job that can show the message below is running at 09:00h and 17:00h.
```text
Daily Status (27/03/2020 - 17:00)
  - To Do : 2 issue(s)
  - In Progress : 3 issue(s)
  - Testing : 1 issue(s)
  - Done : 2 issue(s)
```

The job that can show the message below is running each 30 minutes.

```text
New Comments
  - Issue PBI-1234 - Login page error on load ( https://jira.com.br/browse/PBI-1234 )
    - Comment (0) : This issue needs more information
New State
  - PBI-1245 was in To Do now is In Progress
```

The job that can show the message below is running each 30 minutes.

```text
Issue(s) Added
    - PBI-5330 - New Feature on report page ( https://jira.com.br/browse/PBI-5330 )
Issue(s) Deleted
    - PBI-6530 - Chart with problem
```
