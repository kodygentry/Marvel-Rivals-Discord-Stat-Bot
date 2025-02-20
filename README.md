# Marvel-Rivals-Discord-Stat-Bot
Marvel Rivals Discord stat bot to lookup player stats like history, top hero playtime and general stats

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