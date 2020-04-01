from unittest import TestCase, mock, main
from mockito import *
from mockito import ANY
import sys, os, sqlite3
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.Database import Database
from src.Issue import Issue

class DatabaseTest(TestCase):

    __DATA_LIST = [("PBI-0001","In Progress","Issue number one",0,True),
                 ("PBI-0002","To Do","Issue number two",1,True),
                 ("PBI-0003","Done","Issue number three",100,False)]
    
    __DATA_ONE_RESULT = ("PBI-0001","In Progress","Issue number one",0,True)

    def __createDatabaseObject(self):
        connection = mock()
        when(sqlite3).connect(ANY).thenReturn(connection)

        cursor = mock()
        when(connection).cursor().thenReturn(cursor)

        when(cursor).execute(ANY)
        
        return Database(), cursor

    def __createIssuesExpected(self):
        expected1 = self.__createIssue("PBI-0001", "Issue number one", "In Progress", 0, True)
        expected2 = self.__createIssue("PBI-0002", "Issue number two", "To Do", 1, True)
        expected3 = self.__createIssue("PBI-0003", "Issue number three", "Done", 100, False)
        
        return expected1, expected2, expected3

    def __createIssue(self, key='', summary='', status='', numberOfComments=0, isBacklog=False):
        expected = Issue()
        expected.setIssue(key)
        expected.setSummary(summary)
        expected.setState(status)
        expected.setNumberOfComments(numberOfComments)
        expected.setBacklog(isBacklog)
        return expected

    def __compareIssues(self, issueResult, issueSubject):
        self.assertEqual(issueResult.getIssue(), issueSubject.getIssue())
        self.assertEqual(issueResult.getSummary(), issueSubject.getSummary())
        self.assertEqual(issueResult.getState(), issueSubject.getState())
        self.assertEqual(issueResult.getNumberOfComments(), issueSubject.getNumberOfComments())
        self.assertEqual(issueResult.isBacklog(), issueSubject.isBacklog())

    def test_formatResults_three_results(self):
        db, cursor  = self.__createDatabaseObject()

        when(cursor).fetchall().thenReturn(self.__DATA_LIST)

        resultFormatted = db.findAll()
        expt1, expt2, expt3 = self.__createIssuesExpected()

        self.__compareIssues(resultFormatted[0], expt1)
        self.__compareIssues(resultFormatted[1], expt2)
        self.__compareIssues(resultFormatted[2], expt3)
        self.assertEqual(len(resultFormatted), 3)
    
    def test_formatResults_none_result(self):
        db, cursor  = self.__createDatabaseObject()

        when(cursor).fetchall().thenReturn(None)

        resultFormatted = db.findAll()

        self.assertEqual(resultFormatted, None)

    def test_formatResults_one_result(self):
        db, cursor  = self.__createDatabaseObject()

        when(cursor).fetchall().thenReturn(self.__DATA_ONE_RESULT)

        resultFormatted = db.findAll()
        expt1, _, _ = self.__createIssuesExpected()

        self.__compareIssues(resultFormatted[0], expt1)
        self.assertEqual(len(resultFormatted), 1)
        
    def test_sync_for_the_first_time(self):
        db, cursor  = self.__createDatabaseObject()

        issue1 = self.__createIssue("PBI-0001", "Issue number one", "In Progress", 0, True)
        issue2 = self.__createIssue("PBI-0002", "Issue number two", "Done", 10, False)
        issue3 = self.__createIssue("PBI-0003", "Issue number three", "In Progress", 50, True)
        issuesBacklogJira = [issue1, issue3]
        issuesAllJira = [issue1, issue2, issue3]
        issuesDB = []

        updated, deleted, added = db.sync(issuesDB, issuesBacklogJira, issuesAllJira)

        self.assertEqual(len(updated), 0)
        self.assertEqual(len(deleted), 0)
        self.assertEqual(len(added), 3)
        self.__compareIssues(added[0], issue1)
        self.__compareIssues(added[1], issue2)
        self.__compareIssues(added[2], issue3)

    def test_sync_adding(self):
        db, cursor  = self.__createDatabaseObject()

        issue1 = self.__createIssue("PBI-0001", "Issue number one", "In Progress", 0, True)
        issue2 = self.__createIssue("PBI-0002", "Issue number two", "Done", 10, False)
        issue3 = self.__createIssue("PBI-0003", "Issue number three", "In Progress", 50, True)
        issuesBacklogJira = [issue1, issue3]
        issuesAllJira = [issue1, issue2, issue3]
        issuesDB = [issue1, issue2]

        updated, deleted, added = db.sync(issuesDB, issuesBacklogJira, issuesAllJira)

        self.assertEqual(len(updated), 0)
        self.assertEqual(len(deleted), 0)
        self.assertEqual(len(added), 1)
        self.__compareIssues(added[0], issue3)

    def test_sync_removing(self):
        db, cursor  = self.__createDatabaseObject()

        issue1 = self.__createIssue("PBI-0001", "Issue number one", "In Progress", 0, True)
        issue2 = self.__createIssue("PBI-0002", "Issue number two", "Done", 10, False)
        issue3 = self.__createIssue("PBI-0003", "Issue number three", "In Progress", 50, True)
        issuesBacklogJira = [issue1]
        issuesAllJira = [issue1]
        issuesDB = [issue1, issue2, issue3]

        updated, deleted, added = db.sync(issuesDB, issuesBacklogJira, issuesAllJira)

        self.assertEqual(len(updated), 0)
        self.assertEqual(len(deleted), 2)
        self.assertEqual(len(added), 0)
        self.__compareIssues(deleted[0], issue2)
        self.__compareIssues(deleted[1], issue3)
    
    def test_sync_updating(self):
        db, cursor  = self.__createDatabaseObject()
        
        issue1 = self.__createIssue("PBI-0001", "Issue number one", "In Progress", 0, True)
        issue2 = self.__createIssue("PBI-0002", "Issue number two", "Done", 10, False)
        issue3 = self.__createIssue("PBI-0003", "Issue number three", "In Progress", 50, True)

        issue1_withStatusUpdated = self.__createIssue("PBI-0001", "Issue number one", "In Progress", 0, False)
        issue2_withStatusUpdated = self.__createIssue("PBI-0002", "Issue number two", "Done", 10, True)

        issuesBacklogJira = [issue3, issue2_withStatusUpdated]
        issuesAllJira = [issue1_withStatusUpdated, issue2_withStatusUpdated, issue3]
        issuesDB = [issue1, issue2, issue3]

        updated, deleted, added = db.sync(issuesDB, issuesBacklogJira, issuesAllJira)

        self.assertEqual(len(updated), 2)
        self.assertEqual(len(deleted), 0)
        self.assertEqual(len(added), 0)
        self.__compareIssues(updated[0], issue1_withStatusUpdated)
        self.__compareIssues(updated[1], issue2_withStatusUpdated)

if __name__ == '__main__':
    main()