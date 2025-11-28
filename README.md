# Legal Clerk RAG Agent

A RAG-based legal assistant that answers zoning law questions by analyzing the Alphaville Zoning Code. The agent identifies relevant clauses, detects conflicts, and provides well-reasoned answers with proper citations.

## Features

- Searches the Alphaville Zoning Code for relevant clauses
- Identifies conflicting rules and exceptions
- Provides clear answers with specific clause citations
- Handles complex legal reasoning and conflict resolution

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key in `.env`:

```
OPENAI_API_KEY=your_api_key_here
```

3. Run the server:

```bash
python server.py --port 8100
```

4. Expose with ngrok (for platform submission):

```bash
ngrok http 8100
```

## Usage

The agent accepts POST requests at `/solve` with legal questions about zoning laws.

Example request:

```json
{
  "query": "Can I build a 3-story residential building in Zone B?",
  "kb_search_url": "https://squid-app-7q77b.ondigitalocean.app/api/api/kb/legal/search"
}
```

Example response:

```json
{
  "thought_process": "I need to check Zone B height limits...",
  "retrieved_context_ids": ["clause_B_2", "clause_B_2_conflict"],
  "final_answer": "It depends on the location. Generally, Zone B allows up to 4 stories...",
  "citation": "clause_B_2 (4 stories general), clause_B_2_conflict (2 stories near R-1)"
}
```
