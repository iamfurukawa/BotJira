from unittest import TestCase, main
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.Issue import *

class JiraManagerTest(TestCase):

    __CD_ISSUE = "PBI-1234"
    __FL_STATE = "In Progress"
    __DS_SUMMARY = "Fix tests"
    __NR_COMMENTS = 10
    __FL_BACKLOG_BOOL = True

    __FL_BACKLOG_INT = 1

    __RESULT_BUILD_TUPLE = ("PBI-1234", "In Progress", "Fix tests", 10, 1)
    __RESULT_TO_STRING = 'Issue: PBI-1234\nState: In Progress\nSummary: Fix tests\nNumber of comments: 10\nIs backlog: 1'
    
    def test_buildTuple(self):
        issue = Issue()
        issue.setIssue(self.__CD_ISSUE)
        issue.setSummary(self.__DS_SUMMARY)
        issue.setState(self.__FL_STATE)
        issue.setNumberOfComments(self.__NR_COMMENTS)
        issue.setBacklog(self.__FL_BACKLOG_BOOL)

        self.assertEqual(issue.buildTuple(), self.__RESULT_BUILD_TUPLE)
    
    def test_toString(self):
        issue = Issue()
        issue.setIssue(self.__CD_ISSUE)
        issue.setSummary(self.__DS_SUMMARY)
        issue.setState(self.__FL_STATE)
        issue.setNumberOfComments(self.__NR_COMMENTS)
        issue.setBacklog(self.__FL_BACKLOG_BOOL)

        self.assertEqual(issue.toString(), self.__RESULT_TO_STRING)

if __name__ == '__main__':
    main()