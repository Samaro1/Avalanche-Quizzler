from .getnstoreq import Databaseq
from . import db

class Logical:
    def __init__(self):
        self.CATEGORY_MODELS = {
            "gaming": Databaseq.GamingQuestion,
            "builders": Databaseq.BuildersQuestion,
            "nfts": Databaseq.NftsQuestion,
        }

    def validate_answer(self, category, question_id, user_answer):
        category = category.lower()
        if category not in self.CATEGORY_MODELS:
            return {"error": "Invalid category"}
        Model = self.CATEGORY_MODELS[category]
        with db.session() as session:
            question = session.get(Model, question_id)
            if not question:
                return {"error": "Question not found"}
            user_answer = user_answer.strip().upper()
            if user_answer not in ["A", "B", "C", "D"]:
                return {"error": "Invalid answer format. Use A, B, C, or D"}
            is_correct = (user_answer == question.correct_answer)
            return is_correct