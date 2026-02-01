"""
Alpha AI Datathon 2025 - Legal Clerk RAG Solution (MAXIMUM OPTIMIZATION)
=========================================================================

Ultra-optimized RAG agent targeting perfect 10/10 score across all evaluation metrics:
- Answer Faithfulness (25%) - Zero hallucination, perfect grounding
- Answer Correctness (35%) - Precise legal conclusions  
- Conflict Detection (25%) - Comprehensive conflict analysis
- Reasoning Quality (15%) - Clear, systematic logic

Key Optimizations:
1. Multi-stage search strategy with conflict-specific queries
2. Systematic conflict detection protocol
3. Enhanced citation extraction and validation
4. Formal legal reasoning structure
5. Edge case coverage checklist
"""

import os
import json
import re
import requests
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat

load_dotenv()
KB_API_URL = ""


def advanced_search_knowledge_base(query: str, search_type: str = "general") -> str:
    """
    Advanced search with enhanced formatting and conflict detection hints.
    """
    global KB_API_URL
    
    if not KB_API_URL:
        return "ERROR: Knowledge base URL not configured"
    
    try:
        # Increased top_k for better coverage
        payload = {"query": query, "top_k": 12}
        response = requests.post(KB_API_URL, json=payload, timeout=35)
        response.raise_for_status()
        data = response.json()
        
        if "results" not in data or not data["results"]:
            return f"SEARCH [{search_type}]: No documents found for '{query}'"
        
        formatted_results = [f"=== {search_type.upper()} SEARCH: '{query}' ==="]
        formatted_results.append(f"Found {len(data['results'])} documents\\n")
        
        for i, result in enumerate(data["results"], 1):
            doc_id = result.get("doc_id", f"unknown_doc_{i}")
            content = result.get("content", "")
            score = result.get("score", 0.0)
            
            # Enhanced conflict detection hints
            conflict_indicators = ["except", "however", "unless", "provided", "subject to", 
                                 "notwithstanding", "conflict", "override", "supersede"]
            has_conflicts = any(indicator in content.lower() for indicator in conflict_indicators)
            
            formatted_results.append(f"DOCUMENT #{i}:")
            formatted_results.append(f"  ID: {doc_id}")
            formatted_results.append(f"  Score: {score:.4f}")
            formatted_results.append(f"  Potential Conflicts: {'YES' if has_conflicts else 'NO'}")
            formatted_results.append(f"  Content: {content}")
            formatted_results.append(f"  {'---' * 20}\\n")
        
        return "\\n".join(formatted_results)
        
    except Exception as e:
        return f"SEARCH ERROR [{search_type}]: {str(e)}"


def create_agent() -> Agent:
    """
    Creates agent with maximum optimization for all evaluation criteria.
    """
    
    instructions = """
You are the ULTIMATE Legal Clerk for Alphaville Zoning Code analysis.

EVALUATION CRITERIA (Must Excel in ALL):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. ANSWER FAITHFULNESS (25%): Zero hallucination, perfect document grounding
2. ANSWER CORRECTNESS (35%): Accurate legal conclusions, proper rule application  
3. CONFLICT DETECTION (25%): Find ALL conflicting rules, explain resolution
4. REASONING QUALITY (15%): Systematic, logical, transparent analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 MANDATORY SEARCH PROTOCOL (Use advanced_search_knowledge_base tool):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. PRIMARY SEARCH: Main terms (zone + use/action + requirements)
2. CONFLICT SEARCH: "conflicts exceptions limitations" + main terms  
3. RESTRICTION SEARCH: "restrictions prohibitions conditions" + main terms
4. BOUNDARY SEARCH: "setbacks boundaries proximity" + main terms
5. EXCEPTION SEARCH: "except unless provided notwithstanding" + main terms
6. PROCEDURE SEARCH: "permit variance approval special" + main terms

PERFORM ALL 6 SEARCHES - This is critical for comprehensive analysis!

⚖️ CONFLICT DETECTION PROTOCOL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTIVELY SEARCH FOR these conflict indicators in ALL documents:
- "except" / "exception"      - "however" / "but"
- "unless" / "provided"       - "subject to" / "conditional"  
- "notwithstanding"          - "conflict" / "supersede"
- "limitation" / "restrict"   - "override" / "prevail"

CONFLICT RESOLUTION HIERARCHY:
1. Specific provisions OVERRIDE general provisions
2. Exception clauses OVERRIDE main rules
3. More restrictive rules typically PREVAIL in zoning
4. Proximity-based rules often take PRECEDENCE
5. Later-enacted rules SUPERSEDE earlier ones (if dated)

🎯 FAITHFULNESS RULES (ZERO HALLUCINATION):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ NEVER state anything not explicitly in retrieved documents
❌ NEVER use general zoning knowledge or assumptions
❌ NEVER infer beyond what documents explicitly state

✅ EVERY factual claim MUST reference specific doc_id
✅ Quote EXACT text from documents (use quotation marks)
✅ If unsure: "Documents do not contain specific information about X"
✅ Distinguish between what documents say vs. don't say

📋 SYSTEMATIC RESPONSE STRUCTURE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**STEP 1: QUESTION ANALYSIS**
Break question into components:
- Zone/Location: [what zone is specified?]
- Action/Use: [what is being proposed?] 
- Context: [any special circumstances?]

**STEP 2: COMPREHENSIVE SEARCH**
Perform all 6 search types listed above. Report each search explicitly.

**STEP 3: DOCUMENT INVENTORY**
List ALL retrieved documents with relevance assessment:
- doc_id: Brief description of content and relevance

**STEP 4: RULE EXTRACTION**  
For each relevant document, extract:
- Main rule: "exact quote"
- Conditions: "exact quote"
- Exceptions: "exact quote"

**STEP 5: CONFLICT ANALYSIS**
Systematically check for conflicts:
- Are there contradictory rules that could apply?
- Which rule takes precedence and WHY?
- What conditions determine applicability?

**STEP 6: LEGAL REASONING**
Apply formal logic:
IF [stated conditions from documents] 
THEN [stated outcome from documents]
ELSE [alternative outcome from documents]

**STEP 7: FINAL DETERMINATION**
State definitive answer with ALL conditions and limitations clearly specified.

**STEP 8: COMPREHENSIVE CITATIONS**
doc_id: "exact supporting quote"
[Include ALL documents that support conclusion]

🔍 QUALITY ASSURANCE CHECKLIST:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Before finalizing response, verify:
□ Performed all 6 search types
□ Every factual claim has doc_id citation  
□ Checked for conflicting rules
□ Explained conflict resolution if conflicts exist
□ Used exact quotes from documents
□ Provided clear, definitive answer
□ Included comprehensive citations
□ No assumptions or general knowledge used

Remember: The Alphaville Zoning Code contains INTENTIONAL conflicts. Finding and properly resolving these conflicts is CRITICAL for evaluation success.
"""

    agent = Agent(
        model=OpenAIChat(
            id="gpt-4o-mini",  # Use the more available model
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.0  # Maximum determinism for consistency
        ),
        tools=[advanced_search_knowledge_base],
        instructions=instructions,
        markdown=True
    )
    
    return agent


def extract_document_ids(agent_response: str) -> List[str]:
    """
    Enhanced document ID extraction with comprehensive pattern coverage.
    """
    # Expanded patterns for all possible document ID formats
    patterns = [
        r'\\b(?:clause|section|article|paragraph|rule|code|provision|regulation)_[A-Za-z0-9_\\-]+\\b',
        r'\\bdoc_[A-Za-z0-9_\\-]+\\b',
        r'\\bunknown_doc_[A-Za-z0-9_\\-]+\\b',
        r'\\bzone_[A-Za-z0-9_\\-]+\\b',
        r'\\bID:\\s*([A-Za-z0-9_\\-]+)',
        r'\\bDocument\\s*#?\\d+:\\s*([A-Za-z0-9_\\-]+)'
    ]
    
    found_ids = []
    seen = set()
    
    for pattern in patterns:
        matches = re.findall(pattern, agent_response, re.IGNORECASE)
        for match in matches:
            # Handle tuple results from group patterns
            doc_id = match[0] if isinstance(match, tuple) else match
            if doc_id.lower() not in seen:
                found_ids.append(doc_id)
                seen.add(doc_id.lower())
    
    return found_ids


def extract_citation(agent_response: str, document_ids: List[str]) -> str:
    """
    Enhanced citation extraction that finds exact quotes and properly formats them.
    """
    citations = []
    
    for doc_id in document_ids:
        # Multiple strategies to find quotes associated with this document
        
        # Strategy 1: Look for doc_id followed by colon and quote
        pattern1 = f"{re.escape(doc_id)}:\\s*[\"']([^\"']+)[\"']"
        match1 = re.search(pattern1, agent_response, re.IGNORECASE | re.DOTALL)
        
        # Strategy 2: Look for quote near doc_id (within 100 characters)
        pattern2 = f"(?:.{{0,100}}{re.escape(doc_id)}.{{0,100}})[\"']([^\"']+)[\"']"
        match2 = re.search(pattern2, agent_response, re.IGNORECASE | re.DOTALL)
        
        # Strategy 3: Look for "exact quote" patterns in same paragraph as doc_id
        paragraphs = agent_response.split('\\n\\n')
        for para in paragraphs:
            if doc_id in para:
                quote_matches = re.findall(r'["\']([^"\']{20,})["\'', para)
                if quote_matches:
                    quote = quote_matches[0][:150]  # Limit length
                    if "..." not in quote and len(quote) > 15:
                        citations.append(f'{doc_id}: "{quote}"')
                        break
        else:
            # If no quote found, include just the document ID
            citations.append(doc_id)
    
    return "; ".join(citations) if citations else "No citations extracted"


def extract_final_answer(response_text: str) -> str:
    """
    Enhanced final answer extraction using multiple sophisticated strategies.
    """
    lines = response_text.strip().split('\\n')
    clean_lines = [line.strip() for line in lines if line.strip()]
    
    # Strategy 1: Look for explicit answer markers
    answer_markers = [
        'final determination:', 'final answer:', 'conclusion:', 'answer:', 
        'determination:', 'result:', 'ruling:', 'decision:'
    ]
    
    for line in clean_lines:
        for marker in answer_markers:
            if line.lower().startswith(marker):
                answer = line[len(marker):].strip()
                if len(answer) > 10:
                    return answer
    
    # Strategy 2: Look for definitive legal language
    definitive_patterns = [
        r'^(yes|no),\\s+.{20,}',
        r'^(it depends|conditional|conditionally).{20,}',
        r'^(you can|you cannot|allowed|not allowed|permitted|prohibited).{20,}',
        r'^(the answer is).{20,}',
        r'^(based on|according to).{20,}'
    ]
    
    for line in clean_lines:
        for pattern in definitive_patterns:
            if re.match(pattern, line.lower()):
                return line
    
    # Strategy 3: Look for the most substantive line in final sections
    # Reverse search from end, skipping citations and metadata
    for line in reversed(clean_lines):
        if (len(line) > 50 and 
            not line.startswith(('Document', 'ID:', 'Score:', 'Content:', '**', '##', '- ', '* ')) and
            not re.match(r'^[=\\-·]+$', line) and
            'search' not in line.lower() and
            'citation' not in line.lower()):
            return line
    
    # Strategy 4: Fallback to longest substantive line
    substantive_lines = [
        line for line in clean_lines 
        if len(line) > 30 and not line.startswith(('Document', 'Search', 'ID:', 'Score:'))
    ]
    
    if substantive_lines:
        return max(substantive_lines, key=len)
    
    return "Unable to extract a definitive answer from the legal analysis."


def solve(query: str, search_api_url: str) -> Dict[str, Any]:
    """
    MAXIMUM OPTIMIZATION solve function targeting perfect 10/10 score.
    """
    global KB_API_URL
    KB_API_URL = search_api_url
    
    try:
        agent = create_agent()
        
        # Ultra-optimized query with specific scoring instructions
        optimized_query = f"""
LEGAL ANALYSIS REQUEST: {query}

🎯 EVALUATION TARGET: PERFECT 10/10 SCORE

You will be evaluated on 4 criteria. EXCEL IN ALL:

1. ANSWER FAITHFULNESS (25%): Every claim must cite doc_id. NO general knowledge!
2. ANSWER CORRECTNESS (35%): Precise legal conclusion with proper rule application
3. CONFLICT DETECTION (25%): Find ALL conflicts, explain resolution hierarchy  
4. REASONING QUALITY (15%): Clear systematic logic, comprehensive analysis

CRITICAL SUCCESS FACTORS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 SEARCH REQUIREMENT: Perform ALL 6 search types:
1. Primary: "{query}" (main terms)
2. Conflicts: "conflicts exceptions limitations {query}"
3. Restrictions: "restrictions prohibitions conditions {query}"  
4. Boundaries: "setbacks boundaries proximity {query}"
5. Exceptions: "except unless provided {query}"
6. Procedures: "permit variance approval {query}"

⚖️ CONFLICT DETECTION: 
- Scan EVERY document for: except, however, unless, provided, subject to, notwithstanding
- If conflicts found: Explain which rule prevails and WHY
- If no conflicts: Explicitly state "No conflicting rules found"

📋 MANDATORY RESPONSE SECTIONS:
All sections required for maximum score:

**STEP 1: QUESTION ANALYSIS**
**STEP 2: COMPREHENSIVE SEARCH** (report all 6 searches)
**STEP 3: DOCUMENT INVENTORY** 
**STEP 4: RULE EXTRACTION**
**STEP 5: CONFLICT ANALYSIS** 
**STEP 6: LEGAL REASONING**
**STEP 7: FINAL DETERMINATION**
**STEP 8: COMPREHENSIVE CITATIONS**

Remember: Alphaville Zoning Code has intentional conflicts. Finding them = higher score!
"""

        response = agent.run(optimized_query)
        response_text = str(response)
        
    except Exception as api_error:
        error_str = str(api_error)
        
        # Handle OpenAI API quota/rate limit errors specifically
        if any(term in error_str.lower() for term in ["429", "quota", "rate limit", "insufficient_quota", "billing"]):
            return {
                "thought_process": f"API QUOTA EXCEEDED: The OpenAI API quota has been exhausted. This is a temporary limitation.\n\nOriginal query: {query}\n\nTo resolve this:\n1. Wait for quota reset (usually next billing cycle)\n2. Check OpenAI billing/usage dashboard\n3. Consider upgrading API plan for higher limits\n\nError details: {error_str}",
                "retrieved_context_ids": [],
                "final_answer": "Unable to analyze legal question due to OpenAI API quota limitations. This is a temporary technical issue, not related to the legal question itself. Please try again later or contact system administrator.",
                "citation": "No citations available - API quota exceeded preventing document analysis"
            }
        else:
            # Re-raise other API errors to be handled by outer try-catch
            raise api_error
    
    try:
        
        # Enhanced extraction functions
        document_ids = extract_document_ids(response_text)
        citation = extract_citation(response_text, document_ids)
        final_answer = extract_final_answer(response_text)
        
        # Quality validation
        if len(document_ids) == 0:
            response_text += "\\n\\n⚠️  QUALITY WARNING: No document IDs detected. This may impact scoring."
        
        if "conflict" not in response_text.lower():
            response_text += "\\n\\n⚠️  CONFLICT CHECK: Response may not adequately address potential conflicts."
        
        return {
            "thought_process": response_text,
            "retrieved_context_ids": document_ids,
            "final_answer": final_answer,
            "citation": citation
        }
        
    except Exception as e:
        # Graceful error handling that still provides structure
        error_response = f"SYSTEM ERROR: {str(e)}\\n\\nUnable to complete legal analysis due to technical issues. The Alphaville Zoning Code knowledge base may be inaccessible."
        
        return {
            "thought_process": error_response,
            "retrieved_context_ids": [],
            "final_answer": f"Cannot provide legal guidance due to system error: {str(e)}",
            "citation": "System error - no legal citations available"
        }


if __name__ == "__main__":
    # Test the optimized solution with sample questions
    test_url = "https://squid-app-7q77b.ondigitalocean.app/api/api/kb/legal/search"
    test_queries = [
        "Can I build a 3-story residential building in Zone B?",
        "What is the maximum lot coverage allowed in Zone A-Commercial?",
        "Can I operate a home-based bakery in Zone R-1?"
    ]
    
    print("🏛️  MAXIMUM OPTIMIZATION TEST")
    print("=" * 80)
    print("Testing for: Faithfulness, Correctness, Conflict Detection, Reasoning")
    print("=" * 80)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\\n🔍 TEST {i}: {query}")
        print("-" * 70)
        
        try:
            result = solve(query, test_url)
            
            # Evaluation metrics
            docs_count = len(result['retrieved_context_ids'])
            has_conflicts = 'conflict' in result['thought_process'].lower()
            has_citations = result['citation'] != "No citations extracted"
            answer_length = len(result['final_answer'])
            
            print(f"📊 METRICS:")
            print(f"   Documents Retrieved: {docs_count}")
            print(f"   Conflict Analysis: {'✅' if has_conflicts else '❌'}")
            print(f"   Citations Present: {'✅' if has_citations else '❌'}")
            print(f"   Answer Substantive: {'✅' if answer_length > 50 else '❌'}")
            
            print(f"\\n💡 Answer Preview: {result['final_answer'][:150]}...")
            print(f"🔗 Citation Preview: {result['citation'][:100]}...")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
    
    
    print("\\n🎯 OPTIMIZATION COMPLETE - Ready for 10/10 scoring!")