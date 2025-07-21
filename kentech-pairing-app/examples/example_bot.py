"""
Example bot client that connects to the Kentech Bot Pairing Application.
"""

import asyncio
import json
import websockets
import aiohttp
from typing import Optional


class ExampleBot:
    """Example bot that demonstrates the pairing system integration."""
    
    def __init__(self, name: str, bot_type: str, endpoint: str = "http://localhost:8000"):
        self.name = name
        self.bot_type = bot_type
        self.endpoint = endpoint
        self.bot_id: Optional[str] = None
        self.websocket: Optional[websockets.WebSocketServerProtocol] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self.running = False
    
    async def start(self):
        """Start the bot and register with the pairing system."""
        self.session = aiohttp.ClientSession()
        self.running = True
        
        # Register bot
        await self.register()
        
        # Start WebSocket connection
        if self.bot_id:
            await self.connect_websocket()
    
    async def stop(self):
        """Stop the bot and clean up resources."""
        self.running = False
        
        if self.websocket:
            await self.websocket.close()
        
        if self.session:
            if self.bot_id:
                await self.deregister()
            await self.session.close()
    
    async def register(self):
        """Register the bot with the pairing system."""
        registration_data = {
            "name": self.name,
            "bot_type": self.bot_type,
            "endpoint": f"{self.endpoint}/bot/{self.name}",
            "capabilities": "example,demo,test"
        }
        
        try:
            async with self.session.post(
                f"{self.endpoint}/api/bots",
                json=registration_data
            ) as response:
                if response.status == 201:
                    data = await response.json()
                    self.bot_id = data["id"]
                    print(f"Bot {self.name} registered with ID: {self.bot_id}")
                else:
                    print(f"Failed to register bot: {response.status}")
                    
        except Exception as e:
            print(f"Registration error: {e}")
    
    async def deregister(self):
        """Deregister the bot from the pairing system."""
        try:
            async with self.session.delete(f"{self.endpoint}/api/bots/{self.bot_id}") as response:
                if response.status == 200:
                    print(f"Bot {self.name} deregistered successfully")
                else:
                    print(f"Failed to deregister bot: {response.status}")
        except Exception as e:
            print(f"Deregistration error: {e}")
    
    async def connect_websocket(self):
        """Connect to the WebSocket endpoint."""
        ws_url = f"ws://localhost:8000/ws/bot/{self.bot_id}"
        
        try:
            async with websockets.connect(ws_url) as websocket:
                self.websocket = websocket
                print(f"Bot {self.name} connected to WebSocket")
                
                # Start heartbeat task
                heartbeat_task = asyncio.create_task(self.send_heartbeat())
                
                # Listen for messages
                try:
                    async for message in websocket:
                        await self.handle_message(json.loads(message))
                except websockets.exceptions.ConnectionClosed:
                    print(f"Bot {self.name} WebSocket connection closed")
                finally:
                    heartbeat_task.cancel()
                    
        except Exception as e:
            print(f"WebSocket connection error: {e}")
    
    async def handle_message(self, message: dict):
        """Handle incoming WebSocket messages."""
        message_type = message.get("type")
        
        if message_type == "welcome":
            print(f"Bot {self.name} received welcome message")
            
        elif message_type == "pair_created":
            pair_id = message.get("pair_id")
            primary_bot_id = message.get("primary_bot_id")
            secondary_bot_id = message.get("secondary_bot_id")
            
            if self.bot_id in [primary_bot_id, secondary_bot_id]:
                partner_id = secondary_bot_id if self.bot_id == primary_bot_id else primary_bot_id
                print(f"Bot {self.name} paired with {partner_id} in pair {pair_id}")
                
                # Send a message to the partner
                await self.send_pair_message(partner_id, f"Hello from {self.name}!")
                
        elif message_type == "pair_message":
            from_bot_id = message.get("from_bot_id")
            msg_content = message.get("message")
            print(f"Bot {self.name} received message from {from_bot_id}: {msg_content}")
            
        elif message_type == "pair_terminated":
            print(f"Bot {self.name} pair was terminated")
            
        else:
            print(f"Bot {self.name} received unknown message type: {message_type}")
    
    async def send_heartbeat(self):
        """Send periodic heartbeat messages."""
        while self.running and self.websocket:
            try:
                heartbeat_msg = {
                    "type": "heartbeat",
                    "timestamp": asyncio.get_event_loop().time()
                }
                await self.websocket.send(json.dumps(heartbeat_msg))
                await asyncio.sleep(30)  # Send heartbeat every 30 seconds
            except Exception as e:
                print(f"Heartbeat error: {e}")
                break
    
    async def send_pair_message(self, target_bot_id: str, message: str):
        """Send a message to a paired bot."""
        if self.websocket:
            try:
                pair_msg = {
                    "type": "pair_message",
                    "target_bot_id": target_bot_id,
                    "message": message,
                    "timestamp": asyncio.get_event_loop().time()
                }
                await self.websocket.send(json.dumps(pair_msg))
            except Exception as e:
                print(f"Failed to send pair message: {e}")


async def run_example_bot(name: str, bot_type: str):
    """Run an example bot."""
    bot = ExampleBot(name, bot_type)
    
    try:
        await bot.start()
        
        # Keep the bot running
        while bot.running:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print(f"Stopping bot {name}...")
    finally:
        await bot.stop()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python example_bot.py <bot_name> <bot_type>")
        sys.exit(1)
    
    bot_name = sys.argv[1]
    bot_type = sys.argv[2]
    
    asyncio.run(run_example_bot(bot_name, bot_type))
