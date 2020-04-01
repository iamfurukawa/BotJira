class IssueMock():
    """This file is for simulating a Jira response.
    
    Just use it for testing!

    Jira response structure:
        issue
        issue.key
        issue.fields.status.name
        issue.fields.summary
    """

    key = None
    fields = None

    def __init__(self, key, summary, name):
        self.fields = Fields(summary, name)
        self.key = key
    
    def __repr__(self):
        return repr(self.key)

class Fields:
    status = None
    summary = None

    def __init__(self, summary, name):
        self.status = Status(name)
        self.summary = summary

class Status:
    name = None

    def __init__(self, name):
        self.name = name