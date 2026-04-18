import asyncio
import aiohttp
import sys
import os

# Fix encoding for Windows console
if os.name == 'nt':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

async def create_and_join():
    """Create game and add 2 test bots"""
    try:
        async with aiohttp.ClientSession() as session:
            # Create game
            print("Creating new game...")
            async with session.post(
                'http://localhost:5000/api/game/create',
                json={
                    'user_id': 8000000,
                    'username': 'GameHost'
                }
            ) as resp:
                data = await resp.json()
                game_code = data['game']['code']
                print(f"\n✅ Game created! Code: {game_code}\n")

            # Add 2 test bots
            bots = [
                {'name': 'TestBot1', 'id': 9000001},
                {'name': 'TestBot2', 'id': 9000002}
            ]

            for bot in bots:
                async with session.post(
                    'http://localhost:5000/api/game/join',
                    json={
                        'code': game_code,
                        'user_id': bot['id'],
                        'username': bot['name']
                    }
                ) as resp:
                    data = await resp.json()
                    if 'error' not in data:
                        print(f"✅ {bot['name']} joined")
                    else:
                        print(f"❌ {bot['name']}: {data['error']}")

            print(f"\n🎮 Game ready! Share code: {game_code}")
            print(f"📱 Total players: 3 (You + 2 bots)\n")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    asyncio.run(create_and_join())
