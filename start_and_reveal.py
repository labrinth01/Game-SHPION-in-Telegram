import asyncio
import aiohttp
import sys
import os

# Fix encoding for Windows console
if os.name == 'nt':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

async def start_and_show_roles(game_code):
    """Start game and show all roles"""
    try:
        async with aiohttp.ClientSession() as session:
            # Start game
            print(f"Starting game {game_code}...\n")
            async with session.post(
                f'http://localhost:5000/api/game/{game_code}/start'
            ) as resp:
                data = await resp.json()
                if 'error' in data:
                    print(f"❌ Error: {data['error']}")
                    return

                game = data['game']
                print(f"✅ Game started!")
                print(f"📍 Location: {game['location']}\n")

            # Get roles for all players
            players = [
                {'name': 'GameHost', 'id': 8000000},
                {'name': 'TestBot1', 'id': 9000001},
                {'name': 'TestBot2', 'id': 9000002}
            ]

            print("=" * 50)
            print("ROLES:")
            print("=" * 50)

            for player in players:
                async with session.get(
                    f'http://localhost:5000/api/game/{game_code}/role/{player["id"]}'
                ) as resp:
                    role_data = await resp.json()

                    if role_data['is_spy']:
                        print(f"🕵️  {player['name']} - ШПИОН")
                    else:
                        print(f"👥 {player['name']} - Мирный ({role_data['location']})")

            print("=" * 50)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    game_code = sys.argv[1] if len(sys.argv) > 1 else 'L53X'
    asyncio.run(start_and_show_roles(game_code))
