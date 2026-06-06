# Spec: `generate_response()`

**File:** `generator.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user query and a list of retrieved rule chunks, generate a response that directly answers the question using only the retrieved text as context. The response must be grounded — it should not draw on the model's general knowledge of board games, only on what was retrieved.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's original question |
| `retrieved_chunks` | `list[dict]` | Ranked list of chunks from `retrieve()`, each with `"text"`, `"game"`, and `"distance"` |

**Output:** `str`

A plain string containing the response to show the user. The response should:
- Answer the question using only the retrieved rule text
- Identify which game the answer comes from
- Acknowledge clearly when the answer is not found in the loaded rules

Returns a fallback string (not an error) when `retrieved_chunks` is empty.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Context formatting

*How will you format the retrieved chunks before passing them to the LLM? Describe the structure — not the code. Consider: will you label chunks by game? Include distance scores? Separate chunks with delimiters?*

```
Each chunk gets an indexed label header with game name, followed by chunk text.
One blank line between chunks.

Example:
[1] (Catan)
When a 7 is rolled, no one collects resources...

[2] (Catan)
The robber must be moved to a different terrain hex...

Game name comes from chunk["game"]. Index is 1-based position in the list.
Distance scores not included — not useful to the model.
```

---

### System prompt — grounding instruction

*Write the exact system prompt instruction you will use to prevent the model from answering beyond the retrieved text. This is the most important design decision in this function.*

```
Answer using only the rule text provided below. If the answer is not in the text,
say so clearly — do not guess or draw on outside knowledge.
```

---

### System prompt — citation instruction

*Write the exact instruction you will use to tell the model to identify which game its answer comes from.*

```
State which game your answer comes from, using the game name shown in the chunk label.
```

---

### Fallback behavior

*What should the response say when the answer isn't found in the loaded rule books? Write the exact fallback message.*

```
Keep the existing fallback from the stub (generator.py:32-36):
"I couldn't find anything relevant in the loaded rule books.
Try rephrasing your question — or check that your ingestion pipeline is working."
```

---

### Handling low-relevance chunks

*`retrieved_chunks` may include chunks with high distance scores (weak relevance). Will you filter these out before building context, pass them all in, or handle them another way? What are the tradeoffs?*

```
Pass all chunks through — no second filter. retrieve() already gates at distance <= 0.5.
Double-filtering risks leaving too little context for a useful answer.
```

---

### Message structure

*Describe how you will structure the messages list for the API call — what goes in the system message vs. the user message?*

```
system: grounding instruction + citation instruction (how to behave)

user:   formatted context block (all chunks labeled [N] (Game))
        followed by the question

Example user message:
  Context:
  [1] (Catan)
  When a 7 is rolled...

  [2] (Catan)
  The robber must be moved...

  Question: What happens when you roll a 7?
```

---

## Implementation Notes

*Fill this in after implementing and testing.*

**Test query and response:**

```
Query: [your test query]
Response: [abbreviated response]
Correctly grounded? [yes / no]
Cited the right game? [yes / no]
```

**One thing you changed from your original spec after seeing the actual output:**

```
[your answer here]
```
