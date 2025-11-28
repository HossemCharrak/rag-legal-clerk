"""
FastAPI Server - Legal Clerk RAG Agent API
==========================================

Exposes the Legal Clerk agent as a REST API for the Alpha AI Datathon platform.
Run with: python server.py --port 8100
Submit URL: http://localhost:8100/solve (exposed via ngrok)
"""

import argparse
import uvicorn
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import time

# Import our solution
from solution import solve as solve_function

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Legal Clerk RAG Agent API",
    description="A RAG-based legal assistant for Alphaville Zoning Code questions",
    version="1.0.0"
)

# Add CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SolveRequest(BaseModel):
    """Request model for the solve endpoint"""
    query: Optional[str] = Field(None, description="Legal question to answer")
    claim: Optional[str] = Field(None, description="For factcheck challenge compatibility")
    kb_search_url: str = Field(..., description="Knowledge base search API URL")


class SolveResponse(BaseModel):
    """Response model for the solve endpoint"""
    thought_process: str = Field(..., description="Agent's reasoning process")
    retrieved_context_ids: List[str] = Field(..., description="Document IDs used")
    final_answer: str = Field(..., description="Final answer to the question")
    citation: str = Field(..., description="Citations with quotes")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log all requests for debugging"""
    start_time = time.time()
    
    # Log incoming request
    logger.info(f"Incoming {request.method} request to {request.url.path}")
    
    response = await call_next(request)
    
    # Log response time
    process_time = time.time() - start_time
    logger.info(f"Request completed in {process_time:.2f} seconds")
    
    return response


@app.get("/")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok", 
        "service": "Legal Clerk RAG Agent",
        "endpoint": "/solve",
        "description": "Submit zoning law questions to get AI-powered legal analysis"
    }


@app.get("/health")
async def detailed_health():
    """Detailed health check with system information"""
    import os
    return {
        "status": "healthy",
        "service": "Legal Clerk RAG Agent",
        "version": "1.0.0",
        "endpoints": {
            "solve": "/solve - Main legal question answering endpoint",
            "health": "/health - Detailed health check",
            "docs": "/docs - API documentation"
        },
        "environment": {
            "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
            "python_version": "3.x"
        }
    }


@app.post("/solve", response_model=SolveResponse)
async def solve(request: SolveRequest):
    """
    Main endpoint for answering legal questions about zoning codes.
    
    Accepts a legal question and returns a structured response with:
    - Thought process showing the agent's reasoning
    - List of relevant document IDs from the knowledge base
    - Final answer to the legal question
    - Proper citations with clause IDs and quotes
    """
    try:
        # Log the incoming request
        query = request.query or request.claim
        logger.info(f"Processing legal question: {query[:100]}...")
        
        # Validate request
        if not query:
            raise HTTPException(
                status_code=400, 
                detail="Must provide either 'query' or 'claim' parameter"
            )
        
        if not request.kb_search_url:
            raise HTTPException(
                status_code=400, 
                detail="Must provide 'kb_search_url' parameter"
            )
        
        # Process the request
        logger.info(f"Using knowledge base: {request.kb_search_url}")
        result = solve_function(query, request.kb_search_url)
        
        # Validate response structure
        required_fields = ["thought_process", "retrieved_context_ids", "final_answer", "citation"]
        for field in required_fields:
            if field not in result:
                logger.error(f"Missing required field in response: {field}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Internal error: missing field {field} in response"
                )
        
        # Ensure retrieved_context_ids is a list
        if not isinstance(result["retrieved_context_ids"], list):
            result["retrieved_context_ids"] = []
        
        logger.info(f"Successfully processed request. Found {len(result['retrieved_context_ids'])} relevant documents")
        
        return SolveResponse(**result)
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log and handle unexpected errors
        logger.error(f"Unexpected error processing request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify the service is working"""
    test_request = SolveRequest(
        query="Can I build a residential building in Zone B?",
        kb_search_url="https://squid-app-7q77b.ondigitalocean.app/api/api/kb/legal/search"
    )
    
    try:
        result = await solve(test_request)
        return {
            "status": "success",
            "message": "Test completed successfully",
            "sample_response": {
                "thought_process_length": len(result.thought_process),
                "documents_found": len(result.retrieved_context_ids),
                "has_answer": len(result.final_answer) > 0,
                "has_citation": len(result.citation) > 0
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Test failed: {str(e)}"
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Legal Clerk RAG Agent Server")
    parser.add_argument("--port", type=int, default=8100, help="Port to run the server on")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    args = parser.parse_args()
    
    print(f"""
🏛️  Legal Clerk RAG Agent Server Starting
=========================================
    
Server Details:
- Host: {args.host}
- Port: {args.port}
- API Docs: http://localhost:{args.port}/docs
- Health Check: http://localhost:{args.port}/health
- Main Endpoint: http://localhost:{args.port}/solve

To expose publicly:
1. Keep this server running
2. In another terminal: ngrok http {args.port}
3. Copy the ngrok URL and append /solve
4. Submit: https://xyz.ngrok-free.app/solve

Ready to answer zoning law questions! 🏗️
    """)
    
    uvicorn.run(
        "server:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )