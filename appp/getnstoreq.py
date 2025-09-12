from flask import current_app
from . import db

class Databaseq:
    def __init__(self):
        pass

    # Article Tables
    class Gaming(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        article = db.Column(db.Text, nullable=False)

    class Builders(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        article = db.Column(db.Text, nullable=False)

    class Nfts(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        article = db.Column(db.Text, nullable=False)

    # Summary Tables
    class GamingSummary(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        summary = db.Column(db.Text, nullable=False)
        article_id = db.Column(db.Integer, db.ForeignKey("gaming.id"), nullable=False)

    class BuildersSummary(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        summary = db.Column(db.Text, nullable=False)
        article_id = db.Column(db.Integer, db.ForeignKey("builders.id"), nullable=False)

    class NftsSummary(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        summary = db.Column(db.Text, nullable=False)
        article_id = db.Column(db.Integer, db.ForeignKey("nfts.id"), nullable=False)

    # Question Tables
    class GamingQuestion(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        question = db.Column(db.Text, nullable=False)
        option_a = db.Column(db.Text, nullable=False)
        option_b = db.Column(db.Text, nullable=False)
        option_c = db.Column(db.Text, nullable=False)
        option_d = db.Column(db.Text, nullable=False)
        correct_answer = db.Column(db.String(1), nullable=False)
        summary_id = db.Column(db.Integer, db.ForeignKey("gaming_summary.id"), nullable=False)

    class BuildersQuestion(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        question = db.Column(db.Text, nullable=False)
        option_a = db.Column(db.Text, nullable=False)
        option_b = db.Column(db.Text, nullable=False)
        option_c = db.Column(db.Text, nullable=False)
        option_d = db.Column(db.Text, nullable=False)
        correct_answer = db.Column(db.String(1), nullable=False)
        summary_id = db.Column(db.Integer, db.ForeignKey("builders_summary.id"), nullable=False)

    class NftsQuestion(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        question = db.Column(db.Text, nullable=False)
        option_a = db.Column(db.Text, nullable=False)
        option_b = db.Column(db.Text, nullable=False)
        option_c = db.Column(db.Text, nullable=False)
        option_d = db.Column(db.Text, nullable=False)
        correct_answer = db.Column(db.String(1), nullable=False)
        summary_id = db.Column(db.Integer, db.ForeignKey("nfts_summary.id"), nullable=False)

    def save_summary(self, category, summary_text, article_id):
        with current_app.app_context():
            if category.title() == "Gaming":
                summary_obj = self.GamingSummary(summary=summary_text, article_id=article_id)
                db.session.add(summary_obj)
            elif category.title() == "Builders":
                summary_obj = self.BuildersSummary(summary=summary_text, article_id=article_id)
                db.session.add(summary_obj)
            elif category.title() == "Nfts":
                summary_obj = self.NftsSummary(summary=summary_text, article_id=article_id)
                db.session.add(summary_obj)
            else:
                raise ValueError(f"Unknown category: {category}")
            db.session.commit()
            return summary_obj.id

    def save_question(self, question, category, option_a, option_b, option_c, option_d, correct_answer, summary_id):
        with current_app.app_context():
            if category.title() == "Gaming":
                db.session.add(self.GamingQuestion(
                    question=question,
                    option_a=option_a, option_b=option_b,
                    option_c=option_c, option_d=option_d,
                    correct_answer=correct_answer,
                    summary_id=summary_id
                ))
            elif category.title() == "Builders":
                db.session.add(self.BuildersQuestion(
                    question=question,
                    option_a=option_a, option_b=option_b,
                    option_c=option_c, option_d=option_d,
                    correct_answer=correct_answer,
                    summary_id=summary_id
                ))
            elif category.title() == "Nfts":
                db.session.add(self.NftsQuestion(
                    question=question,
                    option_a=option_a, option_b=option_b,
                    option_c=option_c, option_d=option_d,
                    correct_answer=correct_answer,
                    summary_id=summary_id
                ))
            else:
                raise ValueError(f"Unknown category: {category}")
            db.session.commit()
            print(f"{category} question saved.")

    def get_all_summaries(self, category):
        if category.lower() == "gaming":
            rows = self.GamingSummary.query.all()
        elif category.lower() == "builders":
            rows = self.BuildersSummary.query.all()
        elif category.lower() == "nfts":
            rows = self.NftsSummary.query.all()
        else:
            raise ValueError("Invalid category name")
        return [{"id": r.id, "summary": r.summary, "article_id": r.article_id} for r in rows]

    def get_all_questions(self, category):
        if category.lower() == "gaming":
            rows = self.GamingQuestion.query.all()
        elif category.lower() == "builders":
            rows = self.BuildersQuestion.query.all()
        elif category.lower() == "nfts":
            rows = self.NftsQuestion.query.all()
        else:
            raise ValueError("Invalid category name")
        return [
            {
                "id": r.id,
                "question": r.question,
                "options": [r.option_a, r.option_b, r.option_c, r.option_d],
                "correct_answer": r.correct_answer,
                "summary_id": r.summary_id
            }
            for r in rows
        ]

    def get_all_summ(self, category):
        with current_app.app_context():
            if category.title() == "Builders":
                articles = self.BuildersSummary.query.all()
                if not articles:
                    return None
            elif category.title() == "Gaming":
                articles = self.GamingSummary.query.all()
                if not articles:
                    return None
            elif category.title() == "Nfts":
                articles = self.NftsSummary.query.all()
                if not articles:
                    return None
            return [{"id": row.id, "text": row.summary} for row in articles]

    def get_quiz_questions(self, category, n=3):
        with current_app.app_context():
            model_map = {
                "gaming": self.GamingQuestion,
                "builders": self.BuildersQuestion,
                "nfts": self.NftsQuestion
            }
            model = model_map.get(category.lower())
            if not model:
                raise ValueError(f"Invalid category: {category}")
            rows = model.query.order_by(db.func.random()).limit(n).all()
            result = []
            for row in rows:
                result.append({
                    "id": row.id,
                    "question": row.question,
                    "option_a": row.option_a,
                    "option_b": row.option_b,
                    "option_c": row.option_c,
                    "option_d": row.option_d,
                    "correct_answer": row.correct_answer,
                })
            return result

    def strip_answers(self, question_batch):
        sanitized = []
        for q in question_batch:
            sanitized.append({
                "id": q["id"],
                "question": q["question"],
                "A": q["option_a"],
                "B": q["option_b"],
                "C": q["option_c"],
                "D": q["option_d"],
            })
        return sanitized