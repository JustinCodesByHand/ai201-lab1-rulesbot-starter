from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    TODO — Milestone 3:

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "game"     : the game name
      - "distance" : similarity score (you can use this to filter weak matches)

    Before writing code, talk through these with your group:
      - How will you format the chunks into a context block for the prompt?
      - What instructions will stop the model from answering beyond what the
        rules say? (Grounding is the whole point — a confident wrong answer
        is worse than an honest "I don't know.")
      - How will you surface which game each answer comes from?

    Your response should:
      1. Answer using only the retrieved context — not the model's general knowledge
      2. Make clear which game the answer comes from
      3. Say so clearly when the answer isn't in the loaded rules

    Return the response as a plain string.
    """
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )

    # Your implementation here.
    context_parts = []
    for i, chunk in enumerate(retrieved_chunks):
      context_parts.append(f"[{i+1}] ({chunk['game']})\n{chunk['text']}")

    context = "\n\n".join(context_parts)

    responce = _client.chat.completions.create(
       model=LLM_MODEL,
       messages= [
              {"role": "system", "content":"Answer using only the rule text provided below."
              " If the answer is not in the text, say so clearly — do not guess or draw on "
              "outside knowledge. State which game your answer comes from, using the game name"
              " shown in the chunk label."},
              {"role": "user", "content": f"Context: \n{context}\n\n Question:{query}"},
              ]
    )

    return responce.choices[0].message.content
