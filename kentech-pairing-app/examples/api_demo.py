"""
Example script to demonstrate the Kentech Bot Pairing API.
"""

import asyncio
import aiohttp
import json


async def demo_api():
    """Demonstrate the bot pairing API."""
    base_url = "http://localhost:8000/api"
    
    async with aiohttp.ClientSession() as session:
        print("=== Kentech Bot Pairing API Demo ===\n")
        
        # 1. Check system status
        print("1. Checking system status...")
        async with session.get(f"{base_url}/status") as response:
            status = await response.json()
            print(f"Status: {json.dumps(status, indent=2)}\n")
        
        # 2. Register bots
        print("2. Registering bots...")
        
        bot1_data = {
            "name": "ChatBot-Alpha",
            "bot_type": "chatbot",
            "endpoint": "http://localhost:9001",
            "capabilities": "chat,nlp,conversation"
        }
        
        bot2_data = {
            "name": "TaskBot-Beta",
            "bot_type": "taskbot",
            "endpoint": "http://localhost:9002",
            "capabilities": "tasks,automation,scheduling"
        }
        
        # Register bot 1
        async with session.post(f"{base_url}/bots", json=bot1_data) as response:
            bot1 = await response.json()
            print(f"Registered Bot 1: {bot1['name']} (ID: {bot1['id']})")
        
        # Register bot 2
        async with session.post(f"{base_url}/bots", json=bot2_data) as response:
            bot2 = await response.json()
            print(f"Registered Bot 2: {bot2['name']} (ID: {bot2['id']})\n")
        
        # 3. List all bots
        print("3. Listing all bots...")
        async with session.get(f"{base_url}/bots") as response:
            bots = await response.json()
            for bot in bots:
                print(f"  - {bot['name']} ({bot['bot_type']}) - Status: {bot['status']}")
        print()
        
        # 4. Create a manual pair
        print("4. Creating a manual bot pair...")
        pair_data = {
            "primary_bot_id": bot1["id"],
            "secondary_bot_id": bot2["id"],
            "pairing_strategy": "manual"
        }
        
        async with session.post(f"{base_url}/pairs", json=pair_data) as response:
            if response.status == 201:
                pair = await response.json()
                print(f"Created pair: {pair['id']}")
                print(f"  Primary: {pair['primary_bot']['name']}")
                print(f"  Secondary: {pair['secondary_bot']['name']}")
            else:
                print(f"Failed to create pair: {response.status}")
        print()
        
        # 5. List active pairs
        print("5. Listing active pairs...")
        async with session.get(f"{base_url}/pairs/active") as response:
            pairs = await response.json()
            for pair in pairs:
                print(f"  - Pair {pair['id']}: {pair['primary_bot']['name']} + {pair['secondary_bot']['name']}")
        print()
        
        # 6. Check available strategies
        print("6. Available pairing strategies...")
        async with session.get(f"{base_url}/strategies") as response:
            strategies = await response.json()
            print(f"Strategies: {strategies['strategies']}\n")
        
        # 7. Auto-pair demonstration (register more bots first)
        print("7. Registering additional bots for auto-pairing...")
        
        additional_bots = [
            {"name": "AnalyticsBot-Gamma", "bot_type": "analytics", "endpoint": "http://localhost:9003", "capabilities": "data,analysis,reports"},
            {"name": "NotificationBot-Delta", "bot_type": "notification", "endpoint": "http://localhost:9004", "capabilities": "alerts,messaging,notifications"}
        ]
        
        for bot_data in additional_bots:
            async with session.post(f"{base_url}/bots", json=bot_data) as response:
                if response.status == 201:
                    bot = await response.json()
                    print(f"Registered: {bot['name']}")
        
        # Terminate existing pair first
        if 'pair' in locals():
            print(f"\n8. Terminating existing pair {pair['id']}...")
            async with session.delete(f"{base_url}/pairs/{pair['id']}") as response:
                if response.status == 200:
                    print("Pair terminated successfully")
        
        # Auto-pair with capability-based strategy
        print("\n9. Auto-pairing with capability-based strategy...")
        async with session.post(f"{base_url}/pairs/auto?strategy=capability_based") as response:
            if response.status == 200:
                auto_pairs = await response.json()
                print(f"Created {len(auto_pairs)} automatic pairs:")
                for auto_pair in auto_pairs:
                    print(f"  - {auto_pair['primary_bot']['name']} + {auto_pair['secondary_bot']['name']}")
            else:
                print(f"Auto-pairing failed: {response.status}")
        
        # 10. Final status check
        print("\n10. Final system status...")
        async with session.get(f"{base_url}/status") as response:
            final_status = await response.json()
            print(f"Final Status: {json.dumps(final_status, indent=2)}")


if __name__ == "__main__":
    print("Starting Kentech Bot Pairing API Demo...")
    print("Make sure the pairing application is running on http://localhost:8000")
    print("You can start it with: python main.py\n")
    
    try:
        asyncio.run(demo_api())
    except Exception as e:
        print(f"Demo failed: {e}")
        print("Please ensure the Kentech Bot Pairing Application is running.")
