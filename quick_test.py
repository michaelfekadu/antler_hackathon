#!/usr/bin/env python3
"""
Quick test to verify API posting works.
Run this after starting the server: python3 -m app.main
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Quick API Test\n")
    print("="*60)
    
    # Test 1: Health check
    print("\n1️⃣ Testing API connection...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print("   ✅ API is running!")
        else:
            print(f"   ❌ API returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to API")
        print("   💡 Start the server first: python3 -m app.main")
        return False
    
    # Test 2: Create a user
    print("\n2️⃣ Testing POST /users/ (Create User)...")
    user_data = {
        "telegram_id": f"test_{datetime.now().timestamp()}",
        "name": "Test User",
        "email": "test@example.com"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    if response.status_code == 201:
        user = response.json()
        print(f"   ✅ User created!")
        print(f"   📝 User ID: {user['id']}")
        print(f"   📝 Name: {user['name']}")
        user_id = user['id']
    else:
        print(f"   ❌ Failed: {response.status_code}")
        print(f"   {response.text}")
        return False
    
    # Test 3: Create a goal
    print("\n3️⃣ Testing POST /goals/ (Create Goal)...")
    goal_data = {
        "user_id": user_id,
        "title": "Test Goal - Learn Python",
        "description": "This is a test goal",
        "category": "learning",
        "priority": "high",
        "goal_metadata": {
            "motivation": "Testing the API",
            "test": True
        }
    }
    response = requests.post(f"{BASE_URL}/goals/", json=goal_data)
    if response.status_code == 201:
        goal = response.json()
        print(f"   ✅ Goal created!")
        print(f"   📝 Goal ID: {goal['id']}")
        print(f"   📝 Title: {goal['title']}")
        goal_id = goal['id']
    else:
        print(f"   ❌ Failed: {response.status_code}")
        print(f"   {response.text}")
        return False
    
    # Test 4: Create a conversation message
    print("\n4️⃣ Testing POST /conversations/ (Save Message)...")
    message_data = {
        "user_id": user_id,
        "role": "user",
        "content": "This is a test message from the API test",
        "message_metadata": {"test": True}
    }
    response = requests.post(f"{BASE_URL}/conversations/", json=message_data)
    if response.status_code == 201:
        message = response.json()
        print(f"   ✅ Message saved!")
        print(f"   📝 Message ID: {message['id']}")
        print(f"   📝 Content: {message['content']}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
        print(f"   {response.text}")
        return False
    
    # Test 5: Create a plan
    print("\n5️⃣ Testing POST /plans/ (Create Plan)...")
    plan_data = {
        "user_id": user_id,
        "goal_id": goal_id,
        "plan_content": {
            "overview": "Test plan",
            "phases": [
                {
                    "phase": 1,
                    "title": "Getting Started",
                    "duration": "2 weeks"
                }
            ]
        },
        "generated_by": "test_script"
    }
    response = requests.post(f"{BASE_URL}/plans/", json=plan_data)
    if response.status_code == 201:
        plan = response.json()
        print(f"   ✅ Plan created!")
        print(f"   📝 Plan ID: {plan['id']}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
        print(f"   {response.text}")
        return False
    
    # Test 6: Create a milestone
    print("\n6️⃣ Testing POST /milestones/ (Create Milestone)...")
    milestone_data = {
        "goal_id": goal_id,
        "title": "Test Milestone",
        "description": "Complete the test",
        "status": "pending"
    }
    response = requests.post(f"{BASE_URL}/milestones/", json=milestone_data)
    if response.status_code == 201:
        milestone = response.json()
        print(f"   ✅ Milestone created!")
        print(f"   📝 Milestone ID: {milestone['id']}")
        milestone_id = milestone['id']
    else:
        print(f"   ❌ Failed: {response.status_code}")
        print(f"   {response.text}")
        return False
    
    # Test 7: Update milestone
    print("\n7️⃣ Testing PUT /milestones/ (Update Milestone)...")
    update_data = {"status": "completed"}
    response = requests.put(f"{BASE_URL}/milestones/{milestone_id}", json=update_data)
    if response.status_code == 200:
        print(f"   ✅ Milestone updated!")
    else:
        print(f"   ❌ Failed: {response.status_code}")
        return False
    
    # Test 8: Create check-in
    print("\n8️⃣ Testing POST /checkins/ (Create Check-in)...")
    checkin_data = {
        "user_id": user_id,
        "type": "user_initiated",
        "channel": "telegram_text",
        "sentiment": "positive",
        "conversation_summary": "Test check-in"
    }
    response = requests.post(f"{BASE_URL}/checkins/", json=checkin_data)
    if response.status_code == 201:
        checkin = response.json()
        print(f"   ✅ Check-in created!")
        print(f"   📝 Check-in ID: {checkin['id']}")
    else:
        print(f"   ❌ Failed: {response.status_code}")
        print(f"   {response.text}")
        return False
    
    print("\n" + "="*60)
    print("🎉 ALL TESTS PASSED!")
    print("="*60)
    print(f"\n✅ Successfully tested:")
    print(f"   • User creation (POST)")
    print(f"   • Goal creation (POST)")
    print(f"   • Conversation saving (POST)")
    print(f"   • Plan creation (POST)")
    print(f"   • Milestone creation (POST)")
    print(f"   • Milestone update (PUT)")
    print(f"   • Check-in creation (POST)")
    print(f"\n📊 View the test data in Supabase:")
    print(f"   https://app.supabase.com/project/cqmorgaahmuyxqetxmcd/editor")
    print(f"\n💡 The posting functionality works perfectly!")
    return True

if __name__ == "__main__":
    success = test_api()
    exit(0 if success else 1)

