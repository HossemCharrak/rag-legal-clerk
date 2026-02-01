# Legal Clerk RAG Agent 🏛️

A Retrieval-Augmented Generation (RAG) legal assistant built for the **Alpha AI 2025**. This agent analyzes the Alphaville Zoning Code to answer complex zoning law questions with high accuracy, comprehensive conflict detection, and transparent reasoning.

## 🎯 Project Overview

This solution is optimized for maximum performance across four key evaluation criteria:

| Criterion               | Weight | Focus                                             |
| ----------------------- | ------ | ------------------------------------------------- |
| **Answer Faithfulness** | 25%    | Zero hallucination, perfect document grounding    |
| **Answer Correctness**  | 35%    | Accurate legal conclusions and rule application   |
| **Conflict Detection**  | 25%    | Identifying and resolving conflicting regulations |
| **Reasoning Quality**   | 15%    | Clear, systematic, transparent logic              |

## ✨ Key Features

- **Multi-Stage Search Strategy** - 6-step search process covering general rules, conflicts, restrictions, boundaries, exceptions, and procedures
- **Advanced Conflict Detection** - Actively searches for contradictory rules using legal keywords (except, unless, notwithstanding, etc.)
- **Legal Hierarchy Resolution** - Applies proper precedence rules (specific > general, exceptions > main rules)
- **Citation Pipeline** - Every claim backed by exact document quotes with proper attribution
- **Zero Hallucination** - All responses strictly grounded in retrieved documents

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Client    │─────▶│  FastAPI     │─────▶│   Agent     │
│             │      │  Server      │      │  (GPT-4o)   │
└─────────────┘      └──────────────┘      └─────────────┘
                            │                      │
                            │                      ▼
                            │              ┌──────────────┐
                            │              │  Knowledge   │
                            │              │  Base API    │
                            │              └──────────────┘
                            ▼
                     ┌──────────────┐
                     │  Response    │
                     │  Formatting  │
                     └──────────────┘
```

## 🛠️ Tech Stack

- **Agent Framework**: [agno](https://github.com/agno-framework/agno) v2.0+
- **LLM**: OpenAI GPT-4o-mini (temperature=0.0 for determinism)
- **API Server**: FastAPI + Uvicorn
- **HTTP Client**: Requests
- **Environment**: Python 3.8+

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/HossemCharrak/rag-legal-clerk.git
cd rag-legal-clerk
```

### 2. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=sk-your-api-key-here
```

## 🚀 Usage

### Start the server

```bash
python server.py --port 8100
```

The server will be available at `http://localhost:8100`

### API Endpoints

#### `GET /`

Health check endpoint

**Response:**

```json
{
  "status": "ok",
  "service": "Legal Clerk RAG Agent",
  "endpoint": "/solve"
}
```

#### `GET /health`

Detailed health check with system information

**Response:**

```json
{
  "status": "healthy",
  "service": "Legal Clerk RAG Agent",
  "version": "1.0.0",
  "endpoints": {...},
  "environment": {
    "openai_configured": true
  }
}
```

#### `POST /solve`

Main endpoint for legal question answering

**Request:**

```json
{
  "query": "Can I build a 3-story residential building in Zone B?",
  "kb_search_url": "https://squid-app-7q77b.ondigitalocean.app/api/api/kb/legal/search"
}
```

**Response:**

```json
{
  "thought_process": "**STEP 1: QUESTION ANALYSIS**\n- Zone: Zone B\n- Action: Build 3-story residential building...",
  "retrieved_context_ids": [
    "clause_B_2",
    "clause_B_2_conflict",
    "clause_general_height"
  ],
  "final_answer": "Yes, but with conditions. Zone B generally allows up to 4 stories for residential buildings. However, if your property is within 50 feet of R-1 zoned areas, a 2-story limit applies.",
  "citation": "clause_B_2: 'Residential buildings in Zone B may be up to 4 stories'; clause_B_2_conflict: 'Properties within 50 feet of R-1 zones limited to 2 stories'"
}
```

### Deployment with ngrok

For external access (required for platform submission):

```bash
# In one terminal - run the server
python server.py --port 8100

# In another terminal - expose with ngrok
ngrok http 8100
```

Submit the ngrok URL to the platform (e.g., `https://xyz.ngrok-free.app/solve`)

## 🧪 Testing

Run the test suite:

```bash
python test_agent.py
```

This will test the agent with sample questions and validate response format.

## 📋 Response Format

All responses follow this structure:

- **thought_process**: Detailed step-by-step reasoning following the 8-step protocol
- **retrieved_context_ids**: List of document IDs used in the analysis
- **final_answer**: Clear, definitive answer with all conditions
- **citation**: Exact quotes from documents supporting the conclusion

## 🔍 Search Strategy

The agent performs 6 types of searches for comprehensive coverage:

1. **Primary Search**: Main terms (zone + use/action)
2. **Conflict Search**: Exceptions and limitations
3. **Restriction Search**: Prohibitions and conditions
4. **Boundary Search**: Setbacks and proximity rules
5. **Exception Search**: Legal keywords (except, unless, provided)
6. **Procedure Search**: Permits and special approvals

## ⚙️ Configuration

Key configuration options in `solution.py`:

```python
# LLM settings
model="gpt-4o-mini"
temperature=0.0  # Maximum determinism

# Search settings
top_k=12  # Number of documents to retrieve per search
timeout=35  # Search timeout in seconds
```

## 🐛 Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'agno'`

- **Solution**: Run `pip install -r requirements.txt`

**Issue**: `OPENAI_API_KEY not found`

- **Solution**: Create `.env` file with your API key

**Issue**: Server won't start on port 8100

- **Solution**: Port already in use. Try: `python server.py --port 8200`

**Issue**: Knowledge base API timeout

- **Solution**: Check network connection and KB API URL validity

## 📁 Project Structure

```
rag-legal-clerk/
├── .env                 # Environment variables (gitignored)
├── .gitignore          # Git ignore rules
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── solution.py         # Core RAG agent logic
├── server.py          # FastAPI server
├── test_agent.py      # Test suite
├── deploy.bat         # Windows deployment script
└── deploy.sh          # Linux/Mac deployment script
```

## 📝 License

This project was developed for the Alpha AI Datathon 2025.

## 🤝 Contributing

This is a competition submission. For questions or issues, please open a GitHub issue.

---

**Built with ❤️ for Alpha AI Datathon 2025**
