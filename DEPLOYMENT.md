# 🏛️ Legal Clerk RAG Agent - Deployment Instructions

## Quick Start

Your Legal Clerk RAG Agent is ready to deploy! Follow these steps:

### 1. Start the Server

```bash
# Navigate to the project directory
cd "C:\Users\houss\Desktop\rag-legal-clerk"

# Start the server
python server.py --port 8100
```

The server will start on `http://localhost:8100`

### 2. Expose with ngrok

In a **new terminal window**:

```bash
# Install ngrok if you haven't already
# Download from: https://ngrok.com/download

# Expose your local server
ngrok http 8100
```

You'll see output like:

```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:8100
```

### 3. Submit Your Endpoint

Copy the ngrok URL and append `/solve`:

```
https://abc123.ngrok-free.app/solve
```

Submit this URL to the Alpha AI Datathon platform.

## 🚨 Important Notes

- **Keep both terminals running** during evaluation
- **Don't close ngrok** or your server
- The platform will call your endpoint multiple times
- Monitor requests at http://127.0.0.1:4040 (ngrok web interface)

## Testing Your Agent

Before submitting, test your agent:

```bash
# Run validation
python validate.py

# Test with sample questions
python test_agent.py

# Check the API directly
curl -X POST "http://localhost:8100/solve" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Can I build a 3-story residential building in Zone B?",
    "kb_search_url": "https://squid-app-7q77b.ondigitalocean.app/api/api/kb/legal/search"
  }'
```

## API Documentation

Once your server is running, view the interactive API docs at:

- http://localhost:8100/docs
- http://localhost:8100/health

## Agent Features

Your Legal Clerk RAG Agent provides:

✅ **Intelligent Search**: Searches the Alphaville Zoning Code knowledge base  
✅ **Conflict Detection**: Identifies conflicting regulations  
✅ **Legal Reasoning**: Provides well-reasoned answers with conflict resolution  
✅ **Proper Citations**: Includes specific clause IDs and quoted text  
✅ **Structured Responses**: Returns JSON in the required format

## Sample Response Format

```json
{
  "thought_process": "I need to check Zone B height limits. Let me search for relevant clauses...",
  "retrieved_context_ids": ["clause_B_2", "clause_B_2_conflict"],
  "final_answer": "It depends on the location. Generally, Zone B allows up to 4 stories...",
  "citation": "clause_B_2 (4 stories general), clause_B_2_conflict (2 stories near R-1)"
}
```

## Troubleshooting

### Common Issues

1. **Server won't start**: Check that port 8100 is free
2. **Import errors**: Ensure all dependencies are installed (`pip install -r requirements.txt`)
3. **API key errors**: Verify your `.env` file has a valid OpenAI API key
4. **ngrok issues**: Make sure ngrok is installed and authenticated

### Logs

Monitor server logs for debugging:

- Server logs appear in the terminal where you ran `python server.py`
- ngrok logs appear at http://127.0.0.1:4040

## Support

If you encounter issues:

1. Check the validation script: `python validate.py`
2. Review the server logs for error messages
3. Test individual components with `python test_agent.py`

Good luck with your submission! 🍀
