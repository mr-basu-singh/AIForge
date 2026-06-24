import logging
from groq import Groq
from backend.config import settings

logger = logging.getLogger(__name__)

JUDGE_PROMPT = """You are a strict AI evaluation judge.

You will be given:
- A QUESTION
- An EXPECTED ANSWER
- A GENERATED ANSWER

Score the GENERATED ANSWER on a scale of 0 to 10 based on:
- Accuracy (is it factually correct?)
- Completeness (does it fully answer the question?)
- Helpfulness (is it useful to the user?)

Respond with ONLY a number between 0 and 10. No explanation. No text. Just the number.

QUESTION: {question}
EXPECTED ANSWER: {expected}
GENERATED ANSWER: {generated}

SCORE:"""


class LLMJudge:

    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY missing.")
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.LLM_JUDGE_MODEL

    def score(self, question: str, expected: str, generated: str) -> float:
        try:
            if not generated.strip():
                return 0.0

            prompt = JUDGE_PROMPT.format(
                question=question.strip(),
                expected=expected.strip(),
                generated=generated.strip()
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.0,
            )

            raw = response.choices[0].message.content.strip()

            score = float(raw.split()[0].replace(",", "."))
            score = max(0.0, min(10.0, score))
            return round(score, 2)

        except Exception as e:
            logger.error(f"LLM Judge scoring failed: {e}")
            return 0.0

    def batch_score(self, items: list) -> list:
        """
        items: list of (question, expected, generated) tuples
        returns: list of float scores
        """
        results = []
        for question, expected, generated in items:
            results.append(self.score(question, expected, generated))
        return results