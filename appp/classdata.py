from flask import current_app
from . import db
from .getnstoreq import Databaseq

class Database:
    def __init__(self):
        self.dbq = Databaseq()

    def save_paragraph(self, category, text_list):
        with current_app.app_context():
            if category == "Gaming":
                for text in text_list:
                    db.session.add(self.dbq.Gaming(article=text))
            elif category == "Builders":
                for text in text_list:
                    db.session.add(self.dbq.Builders(article=text))
            elif category == "Nfts":
                for text in text_list:
                    db.session.add(self.dbq.Nfts(article=text))
            else:
                raise ValueError(f"Unknown category: {category}")
            db.session.commit()
            print(f"{category} data saved to database")