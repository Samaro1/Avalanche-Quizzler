import os
from groq import Groq
import json 

MODEL = "llama-3.3-70b-versatile"


class Ainteract:
    def __init__(self):
        # Initialize Groq client
        self.client = Groq(api_key=os.getenv("GROQ_KEY"))



    def summarize_article(self, article_text: str) -> dict:
        """
        Summarize an article into a single JSON paragraph.
        """
        prompt = f"""
        Summarize the following article into a single continuous paragraph that captures the key information in 5 to 7 main ideas.
        Do not use bullet points, lists, or line breaks—keep it as one flowing paragraph.
        Return the result strictly in JSON with this structure:
        {{
          "summary": "Your flattened summary text here."
        }}

        Article:
        {article_text}
        """

        response = self.client.chat.completions.create(
            model=MODEL,
            stream=False,
            messages=[
                {"role": "system", "content": "You are an expert summarizer. Always reply in JSON when asked."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        raw_output = response.choices[0].message.content

        try:
          return json.loads(raw_output)
        
        except json.JSONDecodeError:
        # If it’s not JSON, just return it as plain text
          return {"summary": raw_output}

    def generate_mcqs(self, summary_text):
        """
        Generate 3 multiple-choice questions from the summary.
        """
        prompt = f"""
        Based on the following summary, create 3 multiple-choice questions.
        Each should have 4 options and one correct answer.
        You are a JSON API. Respond ONLY with valid JSON.
        No extra text, no markdown fences.
        The format must be exactly:
        {{
          "questions": [
            {{
              "question": "...",
              "options": ["A", "B", "C", "D"] just input the option, no need for A) option A, B) Option B...,
              "answer": "Correct option alphabet (A, B, C, or D)."
            }}
          ]
        }}

        Summary:
        {summary_text}
        """

        # Ask Groq
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert question generator. Always reply in JSON when asked."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        raw_output = response.choices[0].message.content

        return json.loads(raw_output)