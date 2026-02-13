"""
Simple test script for GPT-enhanced chat endpoint.
"""

import httpx
import json

BASE_URL = "http://127.0.0.1:8000"


async def test_gpt_chat():
    """Test the enhanced chat endpoint with GPT."""
    async with httpx.AsyncClient() as client:
        # Test 1: Chat without prediction context (fallback mode)
        print("Test 1: Chat without MRI context (fallback mode)")
        print("-" * 50)
        payload = {
            "message": "What is a brain MRI?"
        }
        response = await client.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            timeout=15
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Source: {data.get('source', 'unknown')}")
            print(f"Response: {data.get('response', '')[:200]}...")
        print()
        
        # Test 2: Chat with glioma prediction context
        print("Test 2: Chat with Glioma prediction (GPT mode)")
        print("-" * 50)
        payload = {
            "message": "What does glioma mean?",
            "prediction_label": "Glioma Tumor",
            "confidence_score": 0.92
        }
        response = await client.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            timeout=15
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Source: {data.get('source', 'unknown')}")
            print(f"Response: {data.get('response', '')[:200]}...")
        print()
        
        # Test 3: Chat with "No Tumor" prediction
        print("Test 3: Chat with 'No Tumor' prediction")
        print("-" * 50)
        payload = {
            "message": "Is this serious?",
            "prediction_label": "No Tumor",
            "confidence_score": 0.99
        }
        response = await client.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            timeout=15
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Source: {data.get('source', 'unknown')}")
            print(f"Response: {data.get('response', '')[:200]}...")
        print()


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_gpt_chat())
    print("✅ Chat endpoint tests completed!")
