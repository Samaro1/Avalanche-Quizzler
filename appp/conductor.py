from .articlecollect import Article_collector
from .summarizeai import Ainteract
from .getnstoreq import Databaseq
from .logic import Logical

class Conductor:
    def __init__(self):
        self.limit = 3
        self.score = 0

    def sum_n_save(self, list_item, category):
        summarized_list = []
        try:
            for item in list_item:
                article_id = item["id"]
                article_text = item["text"]
                ai = Ainteract()  # Instantiate here
                summar = ai.summarize_article(article_text=article_text)
                summariz = summar.get("summary", "")
                summarized = summariz.replace("\u202f", " ")
                dab = Databaseq()  # Instantiate here
                sum_id = dab.save_summary(
                    category=category,
                    article_id=article_id,
                    summary_text=summarized
                )
                summarized_list.append({"id": sum_id, "text": summarized})
            return summarized_list
        except Exception as e:
            print("Error in sum_n_save:", e)
            return []

    def get_n_save(self, summarized_list, category):
        try:
            for item in summarized_list:
                sum_id = item["id"]
                text = item["text"]
                ai = Ainteract()
                response = ai.generate_mcqs(summary_text=text)
                questions = response.get("questions")
                dab = Databaseq() 
                for q in questions:
                    question = q.get("question")
                    options = q.get("options")
                    answer = q.get("answer")
                    if len(options) >= 4:
                        dab.save_question(
                            category=category,
                            option_a=options[0],
                            option_b=options[1],
                            option_c=options[2],
                            option_d=options[3],
                            question=question,
                            summary_id=sum_id,
                            correct_answer=answer
                        )
        except Exception as e:
            print("Error in get_n_save:", e)

    def get_next_question(self, question_list, index):
        if index < len(question_list):
            items = question_list[index]
            question_data = {
                "question": items["question"],
                "options": {
                    "A": items["option_a"],
                    "B": items["option_b"],
                    "C": items["option_c"],
                    "D": items["option_d"]
                },
                "question_index": index
            }
            return question_data
        else:
            return None