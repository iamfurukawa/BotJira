from unittest import TestCase, mock, main
from unittest.mock import MagicMock
from mockito import * 
from mockito import ANY
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.JiraAPI import JiraAPI
from src.Issue import Issue
import jira as JiraLib
from IssueMock import IssueMock

class JiraAPITest(TestCase):
    def __createJiraMocks(self):
        jiraMock = mock()
        when(JiraLib).JIRA(server = ANY(str), basic_auth = JiraAPI.basic_auth).thenReturn(jiraMock)
        jiraAPI = JiraAPI()

        return jiraMock, jiraAPI

    def __compareIssues(self, issueResult, issueSubject):
        self.assertEqual(issueResult.getIssue(), issueSubject.getIssue())
        self.assertEqual(issueResult.getSummary(), issueSubject.getSummary())
        self.assertEqual(issueResult.getState(), issueSubject.getState())
        self.assertEqual(issueResult.getNumberOfComments(), issueSubject.getNumberOfComments())
        self.assertEqual(issueResult.isBacklog(), issueSubject.isBacklog())

    def __createMockResponseJiraFormatted(self):
        expected1 = Issue()
        expected1.setIssue("PBI-0001")
        expected1.setSummary("First Bug!")
        expected1.setState("To Do")
        expected1.setNumberOfComments(2)
        expected1.setBacklog(False)

        expected2 = Issue()
        expected2.setIssue("PBI-0002")
        expected2.setSummary("Issue number two")
        expected2.setState("To Do")
        expected2.setNumberOfComments(2)
        expected2.setBacklog(False)

        return expected1, expected2

    def test_get_generic_multiple_page(self):
        jiraLib, jiraAPI = self.__createJiraMocks()

        issueFirstIteration = IssueMock('PBI-0001', 'First Bug!', 'To Do')
        issueSecondIteration = IssueMock('PBI-0002', 'Issue number two', 'To Do')
        expt1, expt2 =self.__createMockResponseJiraFormatted()

        when(jiraLib).search_issues(ANY, 0, ANY).thenReturn([issueFirstIteration])
        when(jiraLib).search_issues(ANY, 100, ANY).thenReturn([issueSecondIteration])
        when(jiraLib).search_issues(ANY, 200, ANY).thenReturn([])
        when(jiraLib).comments(ANY).thenReturn(['comment1', 'comment2'])

        results = jiraAPI.getAll()
        
        self.assertEqual(len(results), 2)
        self.__compareIssues(expt1, results[0])
        self.__compareIssues(expt2, results[1])

    def test_get_generic_single_page(self):
        jiraLib, jiraAPI = self.__createJiraMocks()

        issue = IssueMock('PBI-0001', 'First Bug!', 'To Do')
        expt1, _ =self.__createMockResponseJiraFormatted()

        when(jiraLib).search_issues(ANY, 0, ANY).thenReturn([issue])
        when(jiraLib).search_issues(ANY, 100, ANY).thenReturn([])
        when(jiraLib).comments(ANY).thenReturn(['comment1', 'comment2'])

        results = jiraAPI.getAll()
        
        self.assertEqual(len(results), 1)
        self.__compareIssues(expt1, results[0])
        
    def test_get_generic_no_result(self):
        jiraLib, jiraAPI = self.__createJiraMocks()

        when(jiraLib).search_issues(ANY, 0, ANY).thenReturn([])

        results = jiraAPI.getAll()

        self.assertEqual(len(results), 0)
        self.assertEqual(results, [])

if __name__ == '__main__':
    main()