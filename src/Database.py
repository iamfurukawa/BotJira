import sqlite3, os.path
from .Issue import Issue

class Database:
    __conn = None
    __cur = None
    __BASE_DIR = None
    __QUERY_NEW_ISSUE = '''INSERT INTO TB_ISSUES(CD_ISSUE, FL_STATE, DS_SUMMARY, NR_COMMENTS, FL_BACKLOG) VALUES(?,?,?,?,?)'''
    __QUERY_UPDATE_ISSUE = '''UPDATE TB_ISSUES SET CD_ISSUE = ?, FL_STATE = ?, DS_SUMMARY = ?, NR_COMMENTS = ?, FL_BACKLOG = ? WHERE CD_ISSUE = ?'''
    __QUERY_DELETE_ISSUE = '''DELETE FROM TB_ISSUES WHERE CD_ISSUE=?'''
    __QUERY_SEARCH_BY_ID = '''SELECT * FROM TB_ISSUES WHERE CD_ISSUE = ?'''
    __QUERY_SEARCH_ALL_ISSUES = '''SELECT * FROM TB_ISSUES'''

    def __init__(self):
        """Initialize Database."""
        self.__BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.__conn = self.__createConnection()
        self.__cur = self.__conn.cursor()
        print('Sqlite Version: {}'.format(sqlite3.version))

    def __createConnection(self, db_file='issues.db'):
        """Create and open the connection with database.

        Keyword arguments:
        db_file -- The name of db file (default issues.db).
        """       
        db_path = os.path.join(self.__BASE_DIR, db_file)
        try:
            return sqlite3.connect(db_path)
        except Exception as e:
            print('Error at Database.py\n{}'.format(e))
    
    def save(self, issueToSave):
        """Save an Issue on database.

        Keyword arguments:
        issueToSave -- The Issue to save on database.
        """
        self.__executeQuery(self.__QUERY_NEW_ISSUE, issueToSave.buildTuple())

    def update(self, issueToUpdate, idIssue):
        """Update an Issue from database.

        Keyword arguments:
        issueToUpdate -- The Issue to update from database.
        idIssue -- The id of Issue to update.
        """
        self.__executeQuery(self.__QUERY_UPDATE_ISSUE, issueToUpdate.buildTuple() + (idIssue, ))

    def delete(self, idIssue):
        """Delete an Issue from the database.

        Keyword arguments:
        idIssue -- The id of Issue to delete from database.
        """
        self.__executeQuery(self.__QUERY_DELETE_ISSUE, (idIssue,))

    def __executeQuery(self, query, params):
        """Execute a query on database.

        Keyword arguments:
        query -- The query that will be executed.
        params -- The parameters they need to perform operations.
        """
        self.__cur.execute(query, params)
        self.__conn.commit()

    def findAll(self):
        """Returns all Issues from database."""
        self.__cur.execute(self.__QUERY_SEARCH_ALL_ISSUES)
        rows = self.__cur.fetchall()
        return self.__formatResults(rows)
    
    def findById(self, id):
        """Returns one Issues from database.
        
        Keyword arguments:
        id - The id from Issue.
        """
        self.__cur.execute(self.__QUERY_SEARCH_BY_ID, (str(id),))
        row = self.__cur.fetchone()
        return self.__formatResults(row)

    
    def __formatResults(self, results):
        """Returns a list of Issues.
        
        Keyword arguments:
        results - The results from database.
        """
        resultsFormatted = []
        
        if results is None:
            return None

        if type(results) is not list:
            results = [results]
        
        for row in results:
            iss = Issue()
            iss.setIssue(row[0])
            iss.setState(row[1])
            iss.setSummary(row[2])
            iss.setNumberOfComments(row[3])
            iss.setBacklog(row[4])
            resultsFormatted.append(iss)

        return resultsFormatted

    def sync(self, listDB, listBacklog, listEpic):
        """Synchronizes the database with Jira.
        
        Keyword arguments:
        listDB - All the results from database.
        listBacklog - All items in Backlog on Jira.
        listEpic - All items in Epic on Jira.
        """
        fullList = self.__makeListFull(listBacklog, listEpic)
        
        updated, deleted = self.__syncDBToJira(listDB, fullList)
        added = self.__syncJiraToDB(fullList, listDB)

        return updated, deleted, added

    def __makeListFull(self, listBacklog, listEpic):
        """Returns join of list Backlog and Epic.
        
        Keyword arguments:
        listBacklog - All items in Backlog on Jira.
        listEpic - All items in Epic on Jira.
        """
        fullList = []
        for itemEpic in listEpic:
            for itemBacklog in listBacklog:
                if itemEpic.getIssue() == itemBacklog.getIssue():
                    itemEpic.setBacklog(1)
                    fullList.append(itemEpic)
                    break
            else:
                fullList.append(itemEpic)

        return fullList
    
    def __syncDBToJira(self, listDB, fullList):
        """Synchronizes the database based on Jira.
            Updating if it is added on the backlog and remove if it is removed from Epic.
        
        Keyword arguments:
        listDB - All items from Database.
        fullList - All items from Jira.
        """
        itemUpdated = []
        itemDeleted = []

        for itemDB in listDB:
            for itemFull in fullList:
                if itemDB.getIssue() == itemFull.getIssue():
                    if itemDB.isBacklog() != itemFull.isBacklog():
                        itemDB.setBacklog(itemFull.isBacklog())
                        self.update(itemDB, itemDB.getIssue())
                        itemUpdated.append(itemDB)
                    break
            else:
                self.delete(itemDB.getIssue())
                itemDeleted.append(itemDB)
        
        return itemUpdated, itemDeleted
    
    def __syncJiraToDB(self, fullList, listDB):
        """Synchronizes the Jira based on Database.
            Add new items from Jira on Database. Ignore if it already exists.
        
        Keyword arguments:
        listDB - All items from Database.
        fullList - All items from Jira.
        """
        itemAdded = []
        for itemFull in fullList:
            for itemDB in listDB:
                if itemDB.getIssue() == itemFull.getIssue():
                    break
            else:
                self.save(itemFull)
                itemAdded.append(itemFull)
        
        return itemAdded