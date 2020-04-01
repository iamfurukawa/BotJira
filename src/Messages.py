from datetime import datetime

from .Issue import Issue
from .Database import Database
from .JiraAPI import JiraAPI
from .GoogleChatAPI import GoogleChatAPI

class Messages:

    __jiraAPI = None
    __dbase = None
    __gChatAPI = None
    __JIRA_URL = None

    def __init__(self):
        """Initialize Messages."""
        self.__jiraAPI = JiraAPI()
        self.__dbase = Database()
        self.__gChatAPI = GoogleChatAPI()
        self.__JIRA_URL = '<JIRA BASE URL TO BUILD A LINK>'

    def generateDailyReportImpl(self):
        """Create a daily report.

        Template: Daily Status (27/03/2020 - 17:00)
                    - To Do : 2 issue(s)
                    - In Progress : 3 issue(s)
                    - Testing : 1 issue(s)
                    - Done : 2 issue(s)

        The status depend on Jira.
        """
        tasksFromOpenSprint = self.__jiraAPI.getAllFromActualSprint()
        
        if tasksFromOpenSprint is None or len(tasksFromOpenSprint) <= 0:
            return
        
        #Header
        timeNow = datetime.now().strftime('%d/%m/%Y - %H:%M')
        header = '*Daily Status ({})*\n'.format(timeNow)

        #Get All Types
        for task in tasksFromOpenSprint:
            if task.getState() not in states:
                states.append(task.getState())
        
        #Create Message
        body = ''
        for state in states:
            count = 0
            for task in tasksFromOpenSprint:
                if task.getState() == state:
                    count += 1
            body += ' - *{}* : {} issue(s)\n'.format(state, count)
        
        #Create Final Message
        header += body
        header += ' - Total issues: {}\n'.format(len(tasksFromOpenSprint))

        #Send Message
        if len(header) > 0:
            self.__gChatAPI.sendMessage(header)

    def updateCommentsStatusTasksImpl(self):
        """Create a report with the added comments and status changes.

        Template: New Comments
                    - Issue PBI-1234 - Login page error on load ( https://jira.com.br/browse/PBI-1234 )
                    - Comment (0) : This issue needs more information

                    New State
                    - PBI-1245 was in To Do now is In Progress


        The status depend on Jira.
        Just the most recent comments are shown.
        """
        allIssues = self.__jiraAPI.getAll()
        
        #Head
        headComments = '*New Comments*\n'

        #Differences
        bodyComments = ''
        for issue in allIssues:
            dbIssue = self.__dbase.findById(issue.getIssue())
            
            if dbIssue is None or len(dbIssue) < 1:
                continue
            
            if dbIssue[0].getNumberOfComments() != issue.getNumberOfComments():
                bodyComments += ' - *Issue {} - {} ( {}{} )*\n'.format(issue.getIssue(), issue.getSummary(), self.__JIRA_URL, issue.getIssue())
                
                #Get All comments
                comments = self.__jiraAPI.getComments(issue.getIssue())
                commentsReduced = comments[dbIssue[0].getNumberOfComments():]
                for idx, comment in enumerate(commentsReduced):
                    bodyComments += '  - Comment ({}) : {}\n'.format(idx, comment.body.rstrip('\n\r'))
                bodyComments += '\n'
                #Set the new number of comments and update database
                dbIssue[0].setNumberOfComments(issue.getNumberOfComments())
                self.__dbase.update(dbIssue[0], issue.getIssue())
        
        #Head
        headStates = '*New State*\n'

        #Differences
        bodyStates = ''
        for issue in allIssues:
            dbIssue = self.__dbase.findById(issue.getIssue())

            if dbIssue is None or len(dbIssue) < 1:
                continue
            
            if dbIssue[0].getState() != issue.getState():
                bodyStates += ' - *{}* was in _{}_ now is _{}_\n'.format(issue.getIssue(), dbIssue[0].getState(), issue.getState())
                
                #Set the new number of comments and update database
                dbIssue[0].setState(issue.getState())
                self.__dbase.update(dbIssue[0], issue.getIssue())
        
        #Create Final Message
        message = ''
        if len(bodyComments) > 0:
            headComments += bodyComments
            message += headComments
        
        if len(message) > 0:
            message += '\n'

        if len(bodyStates) > 0:
            headStates += bodyStates
            message += headStates
            message += '\n'

        #Send Message
        if len(message) > 0:
            self.__gChatAPI.sendMessage(message)

    def verificationNewIssueImpl(self):
        """Create a report with the issues that are added/removed from Epic.

        Template: Issue(s) Added
                    - PBI-5330 - New Feature on report page ( https://jira.com.br/browse/PBI-5330 )
                Issue(s) Deleted
                    - PBI-6530 - Chart with problem


        In this case the PBI that we need develop are insert into a Epic.
        """
        allIssuesInEpic = self.__jiraAPI.getAll()
        backlogJira = self.__jiraAPI.getAllInBacklog()
        backlogDB = self.__dbase.findAll()
            
        updated, deleted, added = self.__dbase.sync(backlogDB, backlogJira, allIssuesInEpic)
        
        removeBodyMessage = ''
        addBodyMessage = ''
            
        for item in deleted:
            removeBodyMessage += ' - {} - {}\n'.format(item.getIssue(), item.getSummary())

        for item in added:
            addBodyMessage += ' - {} - {} ( {}{} )\n'.format(item.getIssue(), item.getSummary(), self.__JIRA_URL, item.getIssue())

        removeMessage = ''
        addMessage = ''

        if len(deleted) > 0:
            removeMessage = '*Issue(s) Deleted*\n'
            removeMessage += removeBodyMessage
            self.__gChatAPI.sendMessage(removeMessage)

        if len(added) > 0:
            addMessage = '*Issue(s) Added*\n'
            addMessage += addBodyMessage
            self.__gChatAPI.sendMessage(addMessage)
