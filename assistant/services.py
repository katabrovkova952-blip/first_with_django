from openai import OpenAI
from django.conf import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_ai_answer(question, books=None):
    prompt_text = f"Питання користувача: {question}\n\n"

    if books:
        prompt_text += "Інформація про книги:\n\n"
        for book in books:
            prompt_text += (
                f"Назва: {book.title}\n"
                f"Автор: {book.author}\n"
                f"Рік видання: {book.year}\n"
                f"Опис: {book.description}\n\n"
            )

    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Ти асистент, що радить книги на основі каталогу сайту."},
            {"role": "user", "content": prompt_text},
        ], max_completion_tokens=500
    )

    answer = response.choices[0].message.content
    return answer