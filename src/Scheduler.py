import schedule as SchedulerLib
import time
from datetime import date

from .Messages import Messages

class Scheduler:

    __messages = None
    __required = False

    def __init__(self):
        """Initialize Scheduler."""
        self.__messages = Messages()
        self.__needInitialSync(self.__required)
        self.__scheduleTasks()

    def run(self):
        """Execute tasks."""
        while True:
            SchedulerLib.run_pending()
            time.sleep(1)
    
    def __needInitialSync(self, required):
        """Synchronize if need.
        
        Keyword arguments:
        required -- The boolean indicating if need synchronize.
        """
        if required == True:
            print('Synchronizing...')
            allIssuesInEpic = jiraAPI.getAll()
            backlogJira = jiraAPI.getAllInBacklog()
            backlogDB = dbase.findAll()
                
            updated, deleted, added = dbase.sync(backlogDB, backlogJira, allIssuesInEpic)
            print('Sync is Done.')
    
    def __scheduleTasks(self):
        """The task scheduler."""
        SchedulerLib.every().day.at('09:00').do(self.__wrapperGenerateDayliReport)
        SchedulerLib.every().day.at('17:00').do(self.__wrapperGenerateDayliReport)

        SchedulerLib.every().hour.at(":30").do(self.__wrapperVerificationNewIssue)
        SchedulerLib.every().hour.at(":00").do(self.__wrapperVerificationNewIssue)

        SchedulerLib.every().hour.at(":00").do(self.__wrapperUpdateCommentsStatusTasks)
        SchedulerLib.every().hour.at(":30").do(self.__wrapperUpdateCommentsStatusTasks)


    def __wrapperGenerateDayliReport(self):
        """Do some validations before generating the report."""
        print('Executing GenerateDayliReport!')
        if self.__isWeekend():
            print('[Weekend] Skipping Job...')
            return
        self.__messages.generateDailyReportImpl()
        print('Done.')

    def __wrapperVerificationNewIssue(self):
        """Do some validations before generating the report."""
        print('Executing VerificationNewIssue!')
        if self.__isWeekend():
            print('[Weekend] Skipping Job...')
            return
        self.__messages.verificationNewIssueImpl()
        print('Done.')

    def __wrapperUpdateCommentsStatusTasks(self):
        """Do some validations before generating the report."""
        print('Executing UpdateCommentsStatusTasks!')
        if self.__isWeekend():
            print('[Weekend] Skipping Job...')
            return
        self.__messages.updateCommentsStatusTasksImpl()
        print('Done.')

    def __isWeekend(self):
        """Check if today day is in a weekend."""
        return self.__isSaturday() or self.__isSunday()
    
    def __isSaturday(self):
        """Check if today day is Saturday."""
        return date.today().weekday() == 5
    
    def __isSunday(self):
        """Check if today day is Sunday."""
        return date.today().weekday() == 6
