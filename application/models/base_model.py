class BaseModel:
    def __init__(self, db):
        self.db = db

    def save(self, doc):
        return self.db.insert_one(doc)

    def find(self, q):
        return self.db.find(q) or None

    def find_one(self, doc):
        return self.db.find_one(doc) or None