from flask import current_app
from . import db
from .getnstoreq import Databaseq

class Article_collector:
    def __init__(self):
        self.dbq = Databaseq() 
        self.Gaming = self.dbq.Gaming
        self.Builders = self.dbq.Builders
        self.Nfts = self.dbq.Nfts
        self.Nftssum= self.dbq.NftsSummary
        self.Buildsum= self.dbq.BuildersSummary
        self.Gamingsum= self.dbq.GamingSummary

    def get_all_gaming_article(self):
        with current_app.app_context():
            articles = self.Gaming.query.all()
            if not articles:
                return None
            return [{"id": row.id, "text": row.article} for row in articles]

    def get_all_builders_article(self):
        with current_app.app_context():
            articles = self.Builders.query.all()
            if not articles:
                return None
            return [{"id": row.id, "text": row.article} for row in articles]

    def get_all_nfts_article(self):
        with current_app.app_context():
            articles = self.Nfts.query.all()
            if not articles:
                return None
            return [{"id": row.id, "text": row.article} for row in articles]
        
    def get_all_nfts_summary(self):
        with current_app.app_context():
            summaries= self.Nftssum.query.all()
            if not summaries:
                return None
            return [{"id": row.id, "text": row.summary} for row in summaries]
        
    def get_all_builder_summary(self):
        with current_app.app_context():
            summaries= self.Buildsum.query.all()
            if not summaries:
                return None
            return [{"id": row.id, "text": row.summary} for row in summaries]
        
    def get_all_gaming_summary(self):
        with current_app.app_context():
            summaries= self.Gamingsum.query.all()
            if not summaries:
                return None
            return [{"id": row.id, "text": row.summary} for row in summaries]