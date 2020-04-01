import jira
from .Issue import *

class JiraAPI:

    __server = '<JIRA SERVER URL>'
    basic_auth = ('<JIRA USER>', 'JIRA PASSWD')
    __jira = None
    __size = 100

    __SELECT_FROM_EPIC = '''<JQL TO GET ALL PBI FROM EPIC>'''
    __SELECT_FROM_ACTUAL_SPRINT = '''<JQL TO GET ALL OF CURRENT SPRINT>'''
    __SELECT_FROM_BACKLOG = '''<JQL TO GET ALL THE PBI FROM BACKLOG>'''

    def __init__(self):
        """Initialize JiraAPI."""
        self.__jira = jira.JIRA(server = self.__server, basic_auth = self.basic_auth)

    def getAllInBacklog(self):
        """Returns all items in the backlog."""
        return self.__get(self.__SELECT_FROM_BACKLOG, 1)

    def getAll(self):
        """Returns all items."""
        return self.__get(self.__SELECT_FROM_EPIC, 0)

    def getAllFromActualSprint(self):
        """Returns all items from the actual sprint."""
        return self.__get(self.__SELECT_FROM_ACTUAL_SPRINT, 0)

    def getComments(self, issue):
        """Returns all comments from issue.
        
        Keyword arguments:
        issue -- The id of issue.
        """
        return self.__jira.comments(issue)
    
    def __get(self, query, isBacklog):
        """Returns all issues from a jql.
        
        Keyword arguments:
        query -- The query that will be executed.
        isBacklog -- To inform if the flag needs are activated.
        """
        allIssues = []
        initial = 0

        while True:
            start = initial * self.__size
            issues = self.__jira.search_issues(query, start, self.__size)

            if len(issues) == 0:
                break

            initial += 1
            allIssues.extend(issues)

        return self.__dictToListIssue(allIssues, isBacklog)

    def __dictToListIssue(self, issues, isBacklog):
        """Returns a list of Issues.
        
        Keyword arguments:
        issues -- The result of jql in dict.
        isBacklog -- To inform if the flag needs are activated.
        """
        listIssue = []

        for issue in issues:
            comments = self.__jira.comments(issue)
            iss = Issue()
            
            iss.setIssue(issue.key)
            iss.setState(issue.fields.status.name)
            iss.setSummary(issue.fields.summary)
            iss.setNumberOfComments(len(comments))
            iss.setBacklog(isBacklog)

            listIssue.append(iss)
        return listIssue
    

