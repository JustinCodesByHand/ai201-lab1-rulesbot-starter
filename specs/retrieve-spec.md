# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Query approach

*Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?*

```
Call _collection.query() with:
  - query_texts: [query]  — list containing the single query string
  - n_results: n_results  — how many chunks to return
  - include: ["documents", "metadatas", "distances"]
    * documents → chunk text (maps to "text")
    * metadatas → dicts with "game" key (maps to "game")
    * distances → cosine distance scores (maps to "distance")
```

---

### Return structure

*Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?*

```
{
  "text":     results["documents"][0][i],   # the chunk text
  "game":     results["metadatas"][0][i]["game"],  # from stored metadata
  "distance": results["distances"][0][i],   # cosine distance score
}
```

---

### Handling the nested result structure

*`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists.*

```
Use index [0] on each field (documents[0], metadatas[0], distances[0]).

The nesting exists because query_texts accepts a list — you could send
multiple queries at once and get back one result list per query. Since
we only ever send one query, [0] gives us that single query's results.
```

---

### Relevance threshold

*Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?*

```
Filter out chunks with distance > 0.5 (as noted in system-design.md).

Tradeoffs:
  - Filtering: cleaner context, less noise for the LLM, but too tight a
    threshold can drop relevant chunks and leave generate_response() with
    nothing useful.
  - No filtering: guarantees context is always present, but weak matches
    can confuse the LLM into generating answers not grounded in the rules.

generate_response() handles the "nothing found" case when filtering
empties the list.
```

---

### Edge cases

*How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?*

```
(a) Collection empty: early return [] before calling query() — already
    in the stub at retriever.py:68-69.

(b) No good matches: after distance filtering, list may be empty.
    retrieve() returns [] and generate_response() tells the user.
    retrieve() itself does not message the user.

(c) Multi-game results: return all top results as-is, ranked by distance.
    retrieve() does not filter by game — that's attribution work for
    generate_response().
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**Test query and top result returned:**

```
Query: [your test query]
Top result game: [game name]
Distance score: [score]
Does it make sense? [yes / no / explain]
```

**One thing about the query results that surprised you:**

```
[your answer here]
```
