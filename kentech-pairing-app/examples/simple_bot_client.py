
"""
Simple Bot Client - Connect any bot to Kentech Pairing System
Copy this code and modify for your specific bot implementation.
"""

import asyncio
import json
import aiohttp
import websockets
from datetime import datetime


class BotClient:
    """Simple bot client to connect to Kentech Pairing System."""
    
    def __init__(self, name: str, bot_type: str, capabilities: str = ""):
        self.name = name
        self.bot_type = bot_type
        self.capabilities = capabilities
        self.bot_id = None
        self.server_url = "http://localhost:8000"
        self.websocket = None
        self.session = None
        
    async def start(self):
        """Start the bot and connect to pairing system."""
        print(f"🤖 Starting {self.name}...")
        
        # Create HTTP session
        self.session = aiohttp.ClientSession()
        
        try:
            # Register with pairing system
            await self.register()
            
            # Connect WebSocket for real-time communication
            if self.bot_id:
                await self.connect_websocket()
        finally:
            # Clean up session
            if self.session:
                await self.session.close()
    
    async def register(self):
        """Register this bot with the pairing system."""
        registration_data = {
            "name": self.name,
            "bot_type": self.bot_type,
            "endpoint": f"http://localhost:9000/{self.name}",
            "capabilities": self.capabilities
        }
        
        try:
            async with self.session.post(
                f"{self.server_url}/api/bots",
                json=registration_data
            ) as response:
                if response.status == 201:
                    data = await response.json()
                    self.bot_id = data["id"]
                    print(f"✅ {self.name} registered successfully! ID: {self.bot_id}")
                else:
                    error_text = await response.text()
                    print(f"❌ Registration failed: {response.status}")
                    print(f"   Error details: {error_text}")
        except Exception as e:
            print(f"❌ Registration error: {e}")
            print(f"   Make sure the server is running at {self.server_url}")
    
    async def connect_websocket(self):
        """Connect to WebSocket for real-time pairing events."""
        ws_url = f"ws://localhost:8000/ws/bot/{self.bot_id}"
        
        try:
            async with websockets.connect(ws_url) as websocket:
                self.websocket = websocket
                print(f"🔗 {self.name} connected to WebSocket")
                
                # Listen for pairing events
                async for message in websocket:
                    await self.handle_message(json.loads(message))
                    
        except Exception as e:
            print(f"🔌 WebSocket error: {e}")
    
    async def handle_message(self, message):
        """Handle incoming messages from the pairing system."""
        msg_type = message.get("type")
        
        if msg_type == "welcome":
            print(f"👋 {self.name} received welcome from pairing system")
            
        elif msg_type == "pair_created":
            partner_id = message.get("secondary_bot_id") if message.get("primary_bot_id") == self.bot_id else message.get("primary_bot_id")
            print(f"🤝 {self.name} has been paired! Partner ID: {partner_id}")
            
            # Send a greeting to the partner
            await self.send_message_to_partner(partner_id, f"Hello! I'm {self.name}, nice to be paired with you!")
            
        elif msg_type == "pair_message":
            from_bot = message.get("from_bot_id")
            content = message.get("message")
            print(f"💬 {self.name} received message from {from_bot}: {content}")
            
            # Auto-respond
            await self.send_message_to_partner(from_bot, f"Thanks for your message! - {self.name}")
            
        elif msg_type == "pair_terminated":
            print(f"💔 {self.name}'s pair was terminated")
    
    async def send_message_to_partner(self, partner_id: str, message: str):
        """Send a message to paired bot."""
        if self.websocket:
            msg = {
                "type": "pair_message",
                "target_bot_id": partner_id,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            await self.websocket.send(json.dumps(msg))
            print(f"📤 {self.name} sent: {message}")


# Example usage - Run multiple bots
async def run_multiple_bots():
    """Example: Run multiple bots that will auto-pair."""
    
    bots = [
        BotClient("ChatAssistant", "chatbot", "chat,help,conversation"),
        BotClient("TaskManager", "taskbot", "scheduling,automation,tasks"), 
        BotClient("DataAnalyzer", "analytics", "data,analysis,reporting"),
        BotClient("AlertSystem", "notification", "alerts,notifications,monitoring")
    ]
    
    # Start all bots
    tasks = []
    for bot in bots:
        task = asyncio.create_task(bot.start())
        tasks.append(task)
    
    # Wait for all bots to run
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("🚀 Starting Bot Integration Example")
    print("Make sure your Kentech Pairing System is running at http://localhost:8000")
    print("=" * 60)
    
    # Run the example
    asyncio.run(run_multiple_bots())
