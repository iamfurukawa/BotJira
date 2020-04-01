class Issue:
    __CD_ISSUE = None
    __FL_STATE = None
    __DS_SUMMARY = None
    __NR_COMMENTS = None
    __FL_BACKLOG = None

    def setIssue(self, nameIssue):
        """Set the id of the issue."""
        self.__CD_ISSUE = nameIssue

    def setState(self, state):
        """Set the status of the issue."""
        self.__FL_STATE = state

    def setSummary(self, summary):
        """Set the description of the issue."""
        self.__DS_SUMMARY = summary

    def setNumberOfComments(self, numberOfComments):
        """Set the number of comments of the issue."""
        self.__NR_COMMENTS = numberOfComments

    def setBacklog(self, isBacklog):
        """Set the flag indicating if it is in backlog related to the issue."""
        self.__FL_BACKLOG = 1 if isBacklog is True or isBacklog == 1 else 0

    def getIssue(self):
        """Returns the id of the issue."""
        return self.__CD_ISSUE

    def getState(self):
        """Returns the status of the issue."""
        return self.__FL_STATE

    def getSummary(self):
        """Returns the description of the issue."""
        return self.__DS_SUMMARY

    def getNumberOfComments(self):
        """Returns the number of comments of the issue."""
        return self.__NR_COMMENTS

    def isBacklog(self):
        """Returns the flag indicating if it is in backlog related to the issue."""
        return self.__FL_BACKLOG
    
    def buildTuple(self):
        """Returns a tuple with all attributes of the issue."""
        return (self.__CD_ISSUE, self.__FL_STATE, self.__DS_SUMMARY, self.__NR_COMMENTS, self.__FL_BACKLOG)
    
    def toString(self):
        """Returns a String with all attributes formatted ready for printing."""
        return 'Issue: {}\nState: {}\nSummary: {}\nNumber of comments: {}\nIs backlog: {}'.format(self.__CD_ISSUE, self.__FL_STATE, self.__DS_SUMMARY, self.__NR_COMMENTS, self.__FL_BACKLOG)
    