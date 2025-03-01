# Marvel Rivals Discord Bot

A Discord bot designed to fetch and display player statistics, match history, top heroes, and a customizable leaderboard for *Marvel Rivals* using the [tracker.gg API](https://tracker.gg/). Built with Python, Discord.py, and Selenium, this bot provides a convenient way to track player performance directly in Discord.

## Features

- **Player Stats**: Retrieve detailed stats including rank, KDA, win percentage, and more.
- **Match History**: Fetch recent competitive match details with hero usage and performance metrics.
- **Top Heroes**: Display the top 5 most-played heroes for a player with in-depth stats.
- **Leaderboard**: Show a ranked list of players based on their Skill Rating (SR), customizable locally.
- **Help Command**: Quick reference for all available commands.

## Prerequisites

Before running the bot, ensure you have the following installed:

- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Google Chrome**: Required for Selenium to scrape the tracker.gg API.
- **ChromeDriver**: Must match your Chrome version. [Download ChromeDriver](https://chromedriver.chromium.org/downloads) and add it to your system PATH.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kodygentry/marvel-rivals-discord-bot.git
   cd marvel-rivals-discord-bot
2. **Install Dependencies**: Install the required Python packages using pip:
pip install discord.py selenium requests python-dotenv

3. **Set Up Discord Bot Token**:
Create a Discord bot and get its token from the Discord Developer Portal.

- Option 1: Set the token as an environment variable:
Linux/macOS:
export DISCORD_BOT_TOKEN="your_bot_token_here"

Windows (CMD):
set DISCORD_BOT_TOKEN=your_bot_token_here

- Option 2: Use a .env file:
Create a file named .env in the project root:
DISCORD_BOT_TOKEN=your_bot_token_here
The python-dotenv package will load this automatically.

4. **Run the Bot**:
python bot.py
The bot should log in and respond to commands in your Discord server.

## Commands
$stats <username>	Fetches and displays a player's overall stats (rank, KDA, etc.).
$history <number> <username>	Shows the last <number> competitive matches for a player (up to 25).
$top5 <username>	Lists the top 5 most-played heroes for a player with detailed stats.
$leaderboard	Displays a leaderboard of sample players (customize usernames in code).
$help	Shows a list of all available commands with descriptions.

## Usage Example
### Get Player Stats:
$stats kog.
Output: An embed with rank, win percentage, KDA, and more.

### Fetch Match History:
$history 3 kog.
Output: Details of the last 3 matches, including map, hero, and stats.

### View Top Heroes:
$top5 kog.
Output: Top 5 heroes with time played, wins, and performance metrics.

### Check Leaderboard:
$leaderboard
Output: A ranked list of players by SR (edit usernames in bot.py).

## Customization
Leaderboard Players: Edit the usernames list in the $leaderboard command within bot.py to include your desired players:
usernames = ["player1", "player2", "player3"]

## OCR & Top Heroes:
Attach a screenshot and run:

$gg <screenshot>
Output:

The bot lists detected names on separate lines, then displays an embed with each player's top 3 heroes (with win percentage, wins, and losses).
Footer message: Data powered by - KOG!!!!!!!!!

## Error Handling: The bot includes basic error messages; feel free to expand these for more user-friendly responses.

## Screenshots
Here are examples of the bot's output in Discord:

### Stats example
![image](https://github.com/user-attachments/assets/d2213cf5-be1c-4ca6-ac69-57f4ac7e076d)

## Notes
- Dependencies: Requires Chrome and ChromeDriver for Selenium to work. Ensure versions are compatible.
- API Usage: Relies on tracker.gg's unofficial API. Be mindful of rate limits and potential changes to the API structure.
- Performance: Uses threading for the leaderboard to fetch data faster, but Selenium can be slow due to browser automation. Consider optimizing with direct API calls if possible.
- Security: Never commit your .env file or token to GitHub. The .gitignore file excludes it by default.

## Contributing
Feel free to fork this repository, submit issues, or create pull requests with improvements! Suggestions for new features or optimizations are welcome.

## License
This project is open-source and available under the MIT License. Use it freely, but please give credit where due.

## Contact
For questions or support, reach out via GitHub Issues or contact the developer directly (see GitHub profile).

Happy gaming and stat tracking!
