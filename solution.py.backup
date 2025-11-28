"""
Alpha AI Datathon 2025 - Legal Clerk RAG Solution (OPTIMIZED)
===============================================================

An enhanced RAG agent for answering zoning law questions with improved search,
better reasoning, conflict detection, and proper citation of the Alphaville Zoning Code.
"""

import os
import json
import re
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Load environment variables
load_dotenv()

# Global variable for KB API URL
KB_API_URL = ""


def search_knowledge_base(query: str) -> str:
    """
    Search the knowledge base for relevant legal documents and clauses.
    
    This function serves as a tool for the agent to search the Alphaville 
    Zoning Code knowledge base and retrieve relevant documents.
    
    Args:
        query: The search query string
        
    Returns:
        Formatted search results as a string for the agent to process
    """
    global KB_API_URL
    
    if not KB_API_URL:
        return "Error: Knowledge base URL not configured"
    
    try:
        # Make API request to knowledge base with increased top_k for better coverage
        payload = {
            "query": query,
            "top_k": 10  # Increased from 5 for more comprehensive search
        }
        
        response = requests.post(KB_API_URL, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Format results for the agent
        if "results" not in data or not data["results"]:
            return f"No relevant documents found for query: {query}"
        
        formatted_results = []
        for i, result in enumerate(data["results"], 1):
            doc_id = result.get("doc_id", f"doc_{i}")
            content = result.get("content", "No content available")
            score = result.get("score", 0)
            
            formatted_results.append(
                f"Document ID: {doc_id}\n"
                f"Relevance Score: {score:.3f}\n"
                f"Content: {content}\n"
                f"{'=' * 50}"
            )
        
        results_text = "\n".join(formatted_results)
        return f"Search Results for '{query}':\n{results_text}"
        
    except requests.exceptions.RequestException as e:
        return f"Error searching knowledge base: {str(e)}"
    except Exception as e:
        return f"Unexpected error during search: {str(e)}"


def create_agent() -> Agent:
    """
    Create and configure the Legal Clerk RAG agent with enhanced instructions
    for analyzing zoning law questions and detecting conflicts.
    
    Returns:
        Configured Agent instance with optimized settings
    """
    
    # Enhanced instructions with structured reasoning and better guidance
    instructions = """
    You are an expert Legal Clerk specialized in the Alphaville Zoning Code. Your expertise includes 
    legal analysis, conflict resolution, and precise citation of regulations.

    ## PRIMARY WORKFLOW:
    
    1. **COMPREHENSIVE SEARCH**: Use the search_knowledge_base tool with multiple targeted queries:
       - Start with the main question keywords
       - Search for potential exceptions and special cases
       - Look for conflicting regulations
       - Search for specific zones, uses, or requirements mentioned
    
    2. **THOROUGH ANALYSIS**: 
       - Examine ALL retrieved documents carefully
       - Identify general rules vs. specific exceptions
       - Note any conditions, limitations, or special requirements
       - Cross-reference related clauses
    
    3. **CONFLICT DETECTION & RESOLUTION**:
       - Actively look for contradictory regulations
       - When conflicts exist:
         * Cite both conflicting clauses explicitly
         * Determine which takes precedence (specific over general, newer over older)
         * Explain the resolution clearly
         * Include all relevant conditions
    
    4. **PRECISE ANSWERING**:
       - Provide a direct, clear answer to the question
       - Structure your response logically
       - Address all aspects of the question
       - Include specific measurements, numbers, or requirements
    
    5. **COMPREHENSIVE CITATION**:
       - ALWAYS list ALL document IDs you referenced (e.g., clause_B_2, doc_3)
       - Include relevant quoted text from the documents 
       - Show exactly which clause supports which part of your answer
       - Format citations clearly and consistently

    ## RESPONSE STRUCTURE:
    
    Your response should follow this structure:
    
    **Reasoning Process:**
    - What searches you performed
    - What documents you found
    - How you analyzed the regulations
    - Any conflicts discovered and how resolved
    
    **Referenced Documents:**
    - List all document IDs: clause_X, doc_Y, etc.
    
    **Final Answer:**
    - Clear, direct answer to the question
    - Include specific requirements, numbers, conditions
    - Explain any exceptions or special cases
    
    **Citations:**
    - Document ID with relevant quoted text
    - Multiple citations if needed
    - Format: "clause_ID: 'quoted relevant text'"

    ## CRITICAL INSTRUCTIONS:
    
    - ALWAYS search before answering - never rely on general knowledge
    - Search multiple times with different queries if needed
    - Be thorough - missing a relevant clause leads to incorrect answers
    - Pay special attention to words like "except", "unless", "however", "but"
    - When in doubt, search again with refined queries
    - Include specific clause IDs in your final answer
    - Quote the exact text that supports your answer
    
    ## QUALITY CHECKLIST:
    
    Before finalizing your answer, verify:
    ✓ Did I search comprehensively?
    ✓ Did I check for exceptions and conflicts?
    ✓ Does my answer directly address the question?
    ✓ Did I include all relevant document IDs?
    ✓ Did I provide specific citations with quotes?
def extract_document_ids(agent_response: str) -> List[str]:
    """
    Extract document IDs mentioned in the agent's response with improved pattern matching.
    
    Args:
        agent_response: The agent's complete response text
        
    Returns:
        List of unique document IDs found in the response
    """
    # Enhanced patterns to catch more document ID variations
    doc_patterns = [
        r'\bclause_[A-Za-z0-9_\-]+\b',
        r'\bdoc_[A-Za-z0-9_\-]+\b',
        r'\bsection_[A-Za-z0-9_\-]+\b',
        r'\barticle_[A-Za-z0-9_\-]+\b',
        r'\bparagraph_[A-Za-z0-9_\-]+\b',
        r'\brule_[A-Za-z0-9_\-]+\b',
        r'\bcode_[A-Za-z0-9_\-]+\b'
    ]
    
    document_ids = set()
    
    for pattern in doc_patterns:
        matches = re.findall(pattern, agent_response, re.IGNORECASE)
        document_ids.update(matches)
    
    # Return as list maintaining order of first occurrence
    seen = set()
    ordered_ids = []
    for doc_id in re.findall(r'\b(?:clause|doc|section|article|paragraph|rule|code)_[A-Za-z0-9_\-]+\b', 
                             agent_response, re.IGNORECASE):
        if doc_id not in seen:
            seen.add(doc_id)
            ordered_ids.append(doc_id)
    
    return ordered_ids


def extract_citation(agent_response: str, document_ids: List[str]) -> str:
    """
    Extract and format citations with quoted text from the agent's response.
    
    Args:
        agent_response: The agent's complete response text
        document_ids: List of document IDs to look for
        
    Returns:
        Formatted citation string with document IDs and relevant quotes
    """
    citations = []
    
    # Try to find quoted text near each document ID
    for doc_id in document_ids:
        # Look for patterns like: doc_id: "quote" or doc_id states "quote"
        patterns = [
            rf'{re.escape(doc_id)}[:\s]+["\']([^"\']+)["\']',
            rf'["\']([^"\']+)["\'][^.]*{re.escape(doc_id)}',
            rf'{re.escape(doc_id)}[^.]*["\']([^"\']+)["\']'
        ]
        
        quote_found = False
        for pattern in patterns:
            match = re.search(pattern, agent_response, re.IGNORECASE | re.DOTALL)
            if match:
                quote = match.group(1).strip()
                # Limit quote length for readability
                if len(quote) > 100:
                    quote = quote[:97] + "..."
                citations.append(f'{doc_id}: "{quote}"')
                quote_found = True
                break
        
        # If no quote found, just add the document ID
        if not quote_found and doc_id in agent_response:
            citations.append(doc_id)
    
    if not citations and document_ids:
        # Fallback: just list the document IDs
        return ", ".join(document_ids)
    
    return "; ".join(citations)


def extract_final_answer(response_text: str) -> str:
    """
    Extract the final answer from the agent's response with improved parsing.
    
    Args:
        response_text: The complete agent response
        
    Returns:
        The extracted final answer
    """
    # Look for explicit "Final Answer:" section
    final_answer_patterns = [
        r'\*\*Final Answer[:\*]*\s*\n+(.+?)(?:\n\n|\*\*|$)',
        r'Final Answer[:\s]+(.+?)(?:\n\n|\*\*|$)',
        r'Answer[:\s]+(.+?)(?:\n\n|Citation|$)',
    ]
    
    for pattern in final_answer_patterns:
        match = re.search(pattern, response_text, re.IGNORECASE | re.DOTALL)
        if match:
            answer = match.group(1).strip()
            # Clean up the answer
            answer = re.sub(r'\s+', ' ', answer)  # Normalize whitespace
            if len(answer) > 50:  # Reasonable length for an answer
                return answer
    
    # Fallback: extract last substantial paragraph
    lines = response_text.strip().split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    
    for line in reversed(non_empty_lines):
        # Skip lines that look like metadata or section headers
        if (len(line) > 30 and 
            not line.startswith(("Document", "Relevance", "Search Results", "**", "##", "- ", "* ")) and
            not line.startswith("Content:") and
            not re.match(r'^[=\-]+$', line)):
            return line
    
    # Last resort: return last non-empty line
    if non_empty_lines:
        return non_empty_lines[-1]
    
    return "Unable to determine a clear answer from the available information."


def solve(query: str, search_api_url: str) -> Dict[str, Any]:
    """
    Main entry point for the Legal Clerk agent with optimized processing.
    
    Args:
        query: The legal question to answer
        search_api_url: URL of the knowledge base search API
        
    Returns:
        Dictionary with thought_process, retrieved_context_ids, final_answer, and citation
    """
    global KB_API_URL
    KB_API_URL = search_api_url
    
    try:
        # Create the optimized agent
        agent = create_agent()
        
        # Enhanced query prompt with explicit instructions
        agent_query = f"""
        Please answer this zoning law question with thorough analysis: {query}
        
        IMPORTANT INSTRUCTIONS:
        1. Perform multiple searches to find all relevant clauses
        2. Look specifically for exceptions and conflicting rules
        3. Provide a clear, direct answer
        4. List ALL document IDs you reference
        5. Include specific citations with quoted text
        6. Explain any conflicts or special conditions
        
        Structure your response with clear sections for:
        - Reasoning Process
        - Referenced Documents (list all IDs)
        - Final Answer
        - Citations (with quotes)
        """
        
        # Run the agent
        response = agent.run(agent_query)
        
        # Extract information from the agent's response
        response_text = str(response)
        
        # Extract document IDs using improved method
        document_ids = extract_document_ids(response_text)
        
        # Extract citations with quotes
        citation = extract_citation(response_text, document_ids)
        
        # Extract final answer using improved method
        final_answer = extract_final_answer(response_text)
        
        return {
            "thought_process": response_text,
            "retrieved_context_ids": document_ids,
            "final_answer": final_answer,
            "citation": citation if citation else (", ".join(document_ids) if document_ids else "No specific citations found")
        }
        
    except Exception as e:
        return {
            "thought_process": f"Error occurred while processing the query: {str(e)}",
            "retrieved_context_ids": [],
            "final_answer": f"I encountered an error while searching the zoning code: {str(e)}",
            "citation": "Error - no citations available"
        }


if __name__ == "__main__":
    # Test the optimized solution with sample questions
    test_url = "https://squid-app-7q77b.ondigitalocean.app/api/api/kb/legal/search"
    test_queries = [
        "Can I build a 3-story residential building in Zone B?",
        "What is the maximum lot coverage allowed in Zone A-Commercial?",
        "Can I operate a home-based bakery in Zone R-1?"
    ]
    
    print("Testing OPTIMIZED Legal Clerk RAG Agent...")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: {query}")
        print("-" * 40)
        
        try:
            result = solve(query, test_url)
            print(f"Answer: {result['final_answer']}")
            print(f"Citations: {result['citation']}")
            print(f"Documents Used: {result['retrieved_context_ids']}")
        except Exception as e:
            print(f"Error: {e}")