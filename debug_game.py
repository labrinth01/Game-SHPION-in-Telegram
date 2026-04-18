import asyncio
import aiohttp
import sys
import os

# Fix encoding for Windows console
if os.name == 'nt':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

async def debug_game(game_code):
    """Debug game state"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'http://localhost:5000/api/game/{game_code}'
            ) as resp:
                game = await resp.json()

                print("Game State:")
                print("=" * 50)
                print(f"Status: {game.get('status')}")
                print(f"Location: {game.get('location')}")
                print(f"Spy ID: {game.get('spy_id')} (type: {type(game.get('spy_id')).__name__})")
                print(f"\nPlayers:")
                for p in game.get('players', []):
                    print(f"  - {p['username']}: ID={p['id']} (type: {type(p['id']).__name__})")
                print("=" * 50)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    game_code = sys.argv[1] if len(sys.argv) > 1 else 'L53X'
    asyncio.run(debug_game(game_code))
