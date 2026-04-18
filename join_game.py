import asyncio
import aiohttp
import sys
import os

# Fix encoding for Windows console
if os.name == 'nt':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

async def join_game(game_code, player_name, player_id):
    """Join existing game"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'http://localhost:5000/api/game/join',
                json={
                    'code': game_code,
                    'user_id': player_id,
                    'username': player_name
                }
            ) as resp:
                data = await resp.json()
                if 'error' in data:
                    print(f"❌ {player_name}: Error - {data['error']}")
                    return False
                print(f"✅ {player_name} (ID: {player_id}) joined game {game_code}")
                return True
    except Exception as e:
        print(f"❌ {player_name}: Connection error - {e}")
        return False

async def main():
    if len(sys.argv) < 2:
        print("Usage: python join_game.py <GAME_CODE>")
        sys.exit(1)

    game_code = sys.argv[1].upper()

    print(f"\n🎮 Joining game: {game_code}\n")

    # Create 2 test bots
    bots = [
        {'name': 'TestBot1', 'id': 9000001},
        {'name': 'TestBot2', 'id': 9000002}
    ]

    tasks = []
    for bot in bots:
        tasks.append(join_game(game_code, bot['name'], bot['id']))

    results = await asyncio.gather(*tasks)

    success_count = sum(results)
    print(f"\n✨ {success_count}/2 bots joined successfully!\n")

if __name__ == '__main__':
    asyncio.run(main())
