import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestBot:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.game_code = None
        self.is_spy = False
        self.location = None

    async def create_game(self):
        """Create a new game"""
        logger.info(f"{self.name}: Creating game...")
        # Simulate API call to create game
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'http://localhost:5000/api/game/create',
                json={
                    'user_id': self.user_id,
                    'username': self.name
                }
            ) as resp:
                data = await resp.json()
                self.game_code = data['game']['code']
                logger.info(f"{self.name}: Game created with code {self.game_code}")
                return self.game_code

    async def join_game(self, game_code):
        """Join existing game"""
        logger.info(f"{self.name}: Joining game {game_code}...")
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'http://localhost:5000/api/game/join',
                json={
                    'code': game_code,
                    'user_id': self.user_id,
                    'username': self.name
                }
            ) as resp:
                data = await resp.json()
                if 'error' in data:
                    logger.error(f"{self.name}: Error joining game: {data['error']}")
                    return False
                self.game_code = game_code
                logger.info(f"{self.name}: Successfully joined game")
                return True

    async def start_game(self):
        """Start the game"""
        logger.info(f"{self.name}: Starting game...")
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'http://localhost:5000/api/game/{self.game_code}/start'
            ) as resp:
                data = await resp.json()
                if 'error' in data:
                    logger.error(f"{self.name}: Error starting game: {data['error']}")
                    return False
                logger.info(f"{self.name}: Game started")
                return True

    async def get_role(self):
        """Get player role"""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'http://localhost:5000/api/game/{self.game_code}/role/{self.user_id}'
            ) as resp:
                data = await resp.json()
                self.is_spy = data['is_spy']
                self.location = data.get('location')
                role = "ШПИОН" if self.is_spy else f"Мирный ({self.location})"
                logger.info(f"{self.name}: Role = {role}")

    async def vote(self, suspect_id):
        """Vote for a player"""
        logger.info(f"{self.name}: Voting for player {suspect_id}...")
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'http://localhost:5000/api/game/{self.game_code}/vote',
                json={
                    'voter_id': self.user_id,
                    'suspect_id': suspect_id
                }
            ) as resp:
                data = await resp.json()
                if data.get('game_ended'):
                    logger.info(f"{self.name}: Game ended! Winner: {data['result']['winner']}")
                    return data['result']
                else:
                    logger.info(f"{self.name}: Vote recorded ({data.get('votes_count')} votes)")
                    return None

    async def guess_location(self, location):
        """Guess location (spy only)"""
        logger.info(f"{self.name}: Guessing location: {location}...")
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'http://localhost:5000/api/game/{self.game_code}/guess',
                json={
                    'user_id': self.user_id,
                    'location': location
                }
            ) as resp:
                data = await resp.json()
                logger.info(f"{self.name}: Guess result: {data['result']}")
                return data['result']


async def test_game_scenario():
    """Test a complete game scenario"""
    logger.info("=" * 50)
    logger.info("Starting test game scenario...")
    logger.info("=" * 50)

    # Create test bots
    bots = [
        TestBot('TestPlayer1', 1000001),
        TestBot('TestPlayer2', 1000002),
        TestBot('TestPlayer3', 1000003)
    ]

    try:
        # Bot 1 creates game
        game_code = await bots[0].create_game()
        await asyncio.sleep(1)

        # Bots 2 and 3 join
        await bots[1].join_game(game_code)
        await asyncio.sleep(1)
        await bots[2].join_game(game_code)
        await asyncio.sleep(1)

        # Bot 1 starts game
        await bots[0].start_game()
        await asyncio.sleep(1)

        # All bots get their roles
        for bot in bots:
            await bot.get_role()
            await asyncio.sleep(0.5)

        logger.info("\n" + "=" * 50)
        logger.info("Game started! Waiting 5 seconds before voting...")
        logger.info("=" * 50 + "\n")
        await asyncio.sleep(5)

        # Simulate voting - everyone votes for a random player
        logger.info("Starting voting phase...")
        suspect_id = random.choice([bot.user_id for bot in bots])
        logger.info(f"All players will vote for player {suspect_id}")

        result = None
        for bot in bots:
            result = await bot.vote(suspect_id)
            await asyncio.sleep(1)
            if result:
                break

        if result:
            logger.info("\n" + "=" * 50)
            logger.info(f"GAME OVER!")
            logger.info(f"Winner: {result['winner']}")
            logger.info(f"Spy was: {result['spy_name']}")
            logger.info(f"Location: {result['location']}")
            logger.info("=" * 50)

    except Exception as e:
        logger.error(f"Error in test scenario: {e}", exc_info=True)


async def test_spy_guess_scenario():
    """Test spy guessing location"""
    logger.info("=" * 50)
    logger.info("Starting spy guess test scenario...")
    logger.info("=" * 50)

    bots = [
        TestBot('TestPlayer1', 2000001),
        TestBot('TestPlayer2', 2000002),
        TestBot('TestPlayer3', 2000003)
    ]

    try:
        # Create and join game
        game_code = await bots[0].create_game()
        await asyncio.sleep(1)
        await bots[1].join_game(game_code)
        await asyncio.sleep(1)
        await bots[2].join_game(game_code)
        await asyncio.sleep(1)

        # Start game
        await bots[0].start_game()
        await asyncio.sleep(1)

        # Get roles
        spy_bot = None
        for bot in bots:
            await bot.get_role()
            if bot.is_spy:
                spy_bot = bot
            await asyncio.sleep(0.5)

        if spy_bot:
            logger.info(f"\n{spy_bot.name} is the spy! Attempting to guess location...")
            await asyncio.sleep(2)

            # Get available locations
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:5000/api/locations') as resp:
                    locations = await resp.json()
                    if locations:
                        guess = random.choice(locations)['name']
                        result = await spy_bot.guess_location(guess)

                        logger.info("\n" + "=" * 50)
                        logger.info(f"GAME OVER!")
                        logger.info(f"Winner: {result['winner']}")
                        logger.info(f"Spy guessed: {guess}")
                        logger.info(f"Actual location: {result['location']}")
                        logger.info(f"Correct: {result.get('guessed_correct', False)}")
                        logger.info("=" * 50)

    except Exception as e:
        logger.error(f"Error in spy guess scenario: {e}", exc_info=True)


if __name__ == '__main__':
    print("\nTest Bot Simulator")
    print("=" * 50)
    print("1. Test voting scenario")
    print("2. Test spy guess scenario")
    print("=" * 50)

    choice = input("Choose scenario (1 or 2): ").strip()

    if choice == '1':
        asyncio.run(test_game_scenario())
    elif choice == '2':
        asyncio.run(test_spy_guess_scenario())
    else:
        print("Invalid choice")
