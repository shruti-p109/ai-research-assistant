# ollama prompt + response
from ollama import chat

def generate_answer(query, context):
    prompt = f"""
    You are a scientific reasearch assistant.

    Answer the question using ONLY the provided context.

    Provide a concise paragraph summary.

    After every sentence, include the supporting document in square brackets.
    Example:
    Participation in the study may involve pain and bleeding associated with kidney biopsy. [nihms-1761895.pdf]
    More severe complications can include hospitalization and decreased kidney function. [nihms-1761895.pdf]

    Context:
    {context}

    User Question:
    {query}
    """
    response = chat(
        model = 'llama3.1:8b',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    return response['message']['content']
