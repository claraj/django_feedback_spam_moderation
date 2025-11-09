from google import genai
from google.genai.types import GenerateContentConfig

import logging 
logger  = logging.getLogger(__name__)

gemini_client = genai.Client()

def classify_feedback(feedback_text):

    logger.debug(f'Gemini is classifying the following text {feedback_text}')
    response = gemini_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=feedback_text,
        config=GenerateContentConfig(system_instruction="""
You are a content moderation AI for student feedback submissions. 
You will read the student's feedback and classify
the feedback as either "genuine" or "spam".
Reply with one word, either "genuine" or "spam"
""")
    )

    return response.text


if __name__ == '__main__':
    print(classify_feedback('There should be more coffee shops on campus'))  # Should be 'genuine'
    print(classify_feedback('psdjgpidjfghipdfjgh'))  # Should be 'spam'