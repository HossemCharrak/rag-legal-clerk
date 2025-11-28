"""
Test script for the Legal Clerk RAG Agent
=========================================

This script tests the agent with sample questions to ensure it works correctly.
"""

import json
import asyncio
from solution import solve

# Test configuration
TEST_KB_URL = "https://squid-app-7q77b.ondigitalocean.app/api/api/kb/legal/search"

# Sample questions from the challenge
SAMPLE_QUESTIONS = [
    "Can I build a 3-story residential building in Zone B?",
    "What is the maximum lot coverage allowed in Zone A-Commercial?", 
    "Can I operate a home-based bakery in Zone R-1?",
    "What setback requirements apply to corner lots in Zone B?",
    "Are solar panels allowed on historic buildings in the Heritage District?"
]

def test_solution():
    """Test the solution with sample questions"""
    print("🏛️  Testing Legal Clerk RAG Agent")
    print("=" * 50)
    
    for i, question in enumerate(SAMPLE_QUESTIONS, 1):
        print(f"\n📝 Test {i}: {question}")
        print("-" * 60)
        
        try:
            result = solve(question, TEST_KB_URL)
            
            # Print formatted results
            print(f"💭 Thought Process:")
            print(f"   {result['thought_process'][:200]}...")
            
            print(f"\n📚 Documents Used: {len(result['retrieved_context_ids'])}")
            if result['retrieved_context_ids']:
                print(f"   {', '.join(result['retrieved_context_ids'][:3])}...")
            
            print(f"\n✅ Final Answer:")
            print(f"   {result['final_answer']}")
            
            print(f"\n📖 Citation:")
            print(f"   {result['citation']}")
            
            # Validate response format
            required_fields = ["thought_process", "retrieved_context_ids", "final_answer", "citation"]
            missing_fields = [field for field in required_fields if field not in result]
            if missing_fields:
                print(f"❌ Missing fields: {missing_fields}")
            else:
                print("✅ Response format valid")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 60)

def test_api_format():
    """Test that responses match the required API format"""
    print("\n🔍 Testing API Response Format")
    print("=" * 30)
    
    test_question = SAMPLE_QUESTIONS[0]
    result = solve(test_question, TEST_KB_URL)
    
    # Check response structure
    expected_format = {
        "thought_process": str,
        "retrieved_context_ids": list,
        "final_answer": str,
        "citation": str
    }
    
    format_valid = True
    for field, expected_type in expected_format.items():
        if field not in result:
            print(f"❌ Missing field: {field}")
            format_valid = False
        elif not isinstance(result[field], expected_type):
            print(f"❌ Wrong type for {field}: expected {expected_type.__name__}, got {type(result[field]).__name__}")
            format_valid = False
        else:
            print(f"✅ {field}: {expected_type.__name__}")
    
    if format_valid:
        print("\n🎉 API format validation passed!")
    else:
        print("\n❌ API format validation failed!")
    
    # Print sample JSON
    print(f"\n📄 Sample JSON Output:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_solution()
    test_api_format()