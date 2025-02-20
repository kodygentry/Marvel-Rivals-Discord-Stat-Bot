import os
import discord
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import urllib.parse
import requests
import concurrent.futures

# Setup intents for Discord bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Function to fetch player stats
def fetch_player_stats(username):
    driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH
    encoded_username = urllib.parse.quote(username)
    url = f"https://api.tracker.gg/api/v2/marvel-rivals/standard/profile/ign/{encoded_username}/"

    try:
        driver.get(url)
        time.sleep(3)
        page_source = driver.find_element(By.TAG_NAME, "pre").text
        data = json.loads(page_source)

        # Extract stats
        platform_user = data.get("data", {}).get("platformInfo", {}).get("platformUserHandle", "N/A")
        avatar_url = data.get("data", {}).get("platformInfo", {}).get("avatarUrl", "N/A")
        level = data.get("data", {}).get("metadata", {}).get("level", "N/A")

        overview_stats = data.get("data", {}).get("segments", [{}])[0].get("stats", {})
        current_rank = overview_stats.get("ranked", {}).get("metadata", {}).get("tierName", "N/A")
        current_rank_score = overview_stats.get("ranked", {}).get("displayValue", "N/A")
        current_peak_rank = overview_stats.get("peakRanked", {}).get("metadata", {}).get("tierName", "N/A")
        current_peak_rank_score = overview_stats.get("peakRanked", {}).get("displayValue", "N/A")

        lifetime_peak_stats = data.get("data", {}).get("segments", [{}])[1].get("stats", {}).get("lifetimePeakRanked", {})
        all_time_peak_rank = lifetime_peak_stats.get("metadata", {}).get("tierName", "N/A")
        all_time_peak_score = lifetime_peak_stats.get("displayValue", "N/A")
        all_time_season = lifetime_peak_stats.get("metadata", {}).get("seasonShortName", "N/A")

        win_percentage = overview_stats.get("matchesWinPct", {}).get("displayValue", "N/A")
        current_kda = overview_stats.get("kdaRatio", {}).get("displayValue", "N/A")
        time_played = overview_stats.get("timePlayed", {}).get("displayValue", "N/A")

        driver.quit()

        return {
            "platformUser": platform_user,
            "avatarUrl": avatar_url,
            "level": level,
            "currentRank": current_rank,
            "currentRankScore": current_rank_score,
            "currentPeakRank": current_peak_rank,
            "currentPeakRankScore": current_peak_rank_score,
            "allTimePeakRank": all_time_peak_rank,
            "allTimePeakScore": all_time_peak_score,
            "allTimeSeason": all_time_season,
            "winPercentage": win_percentage,
            "currentKDA": current_kda,
            "timePlayed": time_played,
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return None

# Function to fetch match history
def fetch_match_history(username):
    driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH
    encoded_username = urllib.parse.quote(username)
    url = f"https://api.tracker.gg/api/v2/marvel-rivals/standard/matches/ign/{encoded_username}?mode=competitive"

    try:
        driver.get(url)
        time.sleep(3)

        # Extract JSON from the page
        page_source = driver.find_element(By.TAG_NAME, "pre").text
        data = json.loads(page_source)

        # Extract match history
        matches = data.get("data", {}).get("matches", [])
        if not isinstance(matches, list):
            raise ValueError(f"'matches' should be a list but got {type(matches)}")

        match_history = []
        for match in matches[:25]:  # Limit to top 25 matches
            metadata = match.get("metadata", {})
            segments = match.get("segments", [{}])
            overview_segment = segments[0] if len(segments) > 0 else {}
            hero_segment = overview_segment.get("metadata", {})
            heroes = hero_segment.get("heroes", [{}])
            hero_data = heroes[0] if len(heroes) > 0 else {}

            stats = overview_segment.get("stats", {})

            match_info = {
                "mapName": metadata.get("mapName", "Unknown"),
                "modeName": metadata.get("modeName", "N/A"),
                "duration": metadata.get("duration", "N/A"),
                "result": hero_segment.get("outcome", {}).get("result", "N/A"),
                "score": f"{metadata.get('scores', [])[0]} - {metadata.get('scores', [])[1]}" if "scores" in metadata else "N/A",
                "heroName": hero_data.get("name", "Unknown"),
                "heroRole": hero_data.get("roleName", "N/A"),
                "heroImageUrl": hero_data.get("imageUrl", "https://example.com/default-avatar.png"),
                "kills": stats.get("kills", {}).get("displayValue", "N/A"),
                "deaths": stats.get("deaths", {}).get("displayValue", "N/A"),
                "assists": stats.get("assists", {}).get("displayValue", "N/A"),
                "kdRatio": stats.get("kdRatio", {}).get("displayValue", "N/A"),
                "totalHeroDamage": stats.get("totalHeroDamage", {}).get("displayValue", "N/A"),
                "totalHeroHeal": stats.get("totalHeroHeal", {}).get("displayValue", "N/A"),
            }

            match_history.append(match_info)

        driver.quit()

        return match_history if match_history else None

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return None

# Function to fetch top 5 heroes
def fetch_top5(username):
    driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH
    encoded_username = urllib.parse.quote(username.strip())
    url = f"https://api.tracker.gg/api/v2/marvel-rivals/standard/profile/ign/{encoded_username}"

    try:
        driver.get(url)
        time.sleep(3)

        # Extract JSON from the page
        page_source = driver.find_element(By.TAG_NAME, "pre").text
        data = json.loads(page_source)

        # Check if "segments" exist
        segments = data.get("data", {}).get("segments", [])
        if not segments:
            print("No segments found in API response.")
            return None

        # Filter hero segments
        hero_segments = [seg for seg in segments if seg.get("type") == "hero"]
        if not hero_segments:
            print("No hero segments found.")
            return None

        # Sort heroes by time played and take top 5
        top_heroes = sorted(
            hero_segments,
            key=lambda x: x.get("stats", {}).get("timePlayed", {}).get("value", 0),
            reverse=True
        )[:5]

        # Format hero data
        top_heroes_data = []
        for hero in top_heroes:
            stats = hero.get("stats", {})
            metadata = hero.get("metadata", {})
            top_heroes_data.append({
                "name": metadata.get("name", "Unknown"),
                "role": metadata.get("roleName", "N/A"),
                "imageUrl": metadata.get("imageUrl", "https://example.com/default-avatar.png"),
                "timePlayed": stats.get("timePlayed", {}).get("displayValue", "N/A"),
                "matchesPlayed": stats.get("matchesPlayed", {}).get("displayValue", "N/A"),
                "wins": stats.get("matchesWon", {}).get("displayValue", "N/A"),
                "winPercentage": stats.get("matchesWinPct", {}).get("displayValue", "N/A"),
                "kills": stats.get("kills", {}).get("displayValue", "N/A"),
                "deaths": stats.get("deaths", {}).get("displayValue", "N/A"),
                "assists": stats.get("assists", {}).get("displayValue", "N/A"),
                "kda": stats.get("kdaRatio", {}).get("displayValue", "N/A"),
                "totalDamage": stats.get("totalHeroDamage", {}).get("displayValue", "N/A"),
                "totalHeals": stats.get("totalHeroHeal", {}).get("displayValue", "N/A"),
            })

        driver.quit()
        return top_heroes_data

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return None

# Discord bot events
@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$stats'):
        try:
            username = " ".join(message.content.split()[1:])
            if not username:
                await message.channel.send("Please provide a username. Usage: `$stats <username>`")
                return

            await message.channel.send(f"Fetching stats for {username}, please wait...")
            player_data = fetch_player_stats(username)

            if player_data:
                embed = discord.Embed(
                    title=f"Player Stats for {player_data['platformUser']}",
                    color=0x1ABC9C,
                    timestamp=message.created_at,
                )
                embed.set_thumbnail(url=player_data["avatarUrl"])
                embed.add_field(name="Level:", value=f"{player_data['level']}", inline=False)
                embed.add_field(
                    name="Current Season Rank:",
                    value=f"{player_data['currentRank']} - {player_data['currentRankScore']} RS",
                    inline=False,
                )
                embed.add_field(
                    name="Current Season Peak:",
                    value=f"{player_data['currentPeakRank']} - {player_data['currentPeakRankScore']} RS",
                    inline=False,
                )
                embed.add_field(
                    name="All-Time Peak:",
                    value=f"{player_data['allTimePeakRank']} - {player_data['allTimePeakScore']} (Season {player_data['allTimeSeason']})",
                    inline=False,
                )
                embed.add_field(
                    name="Current Season Stats:",
                    value=f"**Win %**: {player_data['winPercentage']}\n"
                          f"**KDA**: {player_data['currentKDA']}\n"
                          f"**Time Played**: {player_data['timePlayed']}",
                    inline=False,
                )
                embed.set_footer(text="API by Kog")
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(f"Failed to fetch stats for {username}.")
        except Exception as e:
            await message.channel.send(f"An error occurred: {e}")

    if message.content.startswith('$history'):
        try:
            args = message.content.split()
            if len(args) < 3:
                await message.channel.send("Please provide the number of matches and the username. Usage: `$history <number_of_matches> <username>`")
                return

            try:
                size = int(args[1])
                if size < 1:
                    await message.channel.send("Number of matches must be at least 1.")
                    return
            except ValueError:
                await message.channel.send("Invalid number of matches. Please provide a valid integer.")
                return

            username = " ".join(args[2:])
            await message.channel.send(f"Fetching match history for {username} (last {size} matches), please wait...")

            match_history = fetch_match_history(username)

            if match_history:
                limited_history = match_history[:size]
                embed = discord.Embed(title=f"Match History for - {username}", color=0x3498DB)
                embed.set_thumbnail(url=limited_history[0].get("heroImageUrl", "https://example.com/default-avatar.png"))

                for i, match in enumerate(limited_history, start=1):
                    result_emoji = "✅" if match['result'].lower() == "win" else "❌"
                    embed.add_field(
                        name=f"Match {i}: {result_emoji}\n{match['mapName']} ({match['modeName']})",
                        value=f"**Result**: {match['result']}\n"
                              f"**Score**: {match['score']}\n"
                              f"**Hero**: {match['heroName']}\n"
                              f"**Kills/Deaths/Assists**: {match['kills']}/{match['deaths']}/{match['assists']}\n"
                              f"**K/D Ratio**: {match['kdRatio']}\n"
                              f"**Total Damage**: {match['totalHeroDamage']}\n"
                              f"**Total Healing**: {match['totalHeroHeal']}\n"
                              "───────────────────────\n",
                        inline=False
                    )
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(f"No match history found for {username}.")
        except Exception as e:
            await message.channel.send(f"An error occurred: {e}")

    if message.content.startswith('$top5'):
        try:
            username = " ".join(message.content.split()[1:])
            if not username:
                await message.channel.send("Please provide a username. Usage: `$top5 <username>`")
                return

            await message.channel.send(f"Fetching top 5 heroes for {username}, please wait...")
            top_heroes = fetch_top5(username)

            if top_heroes:
                embed = discord.Embed(
                    title=f"Top 5 Most Played Heroes for {username} (Current Season)",
                    color=0x9B59B6
                )
                for hero in top_heroes:
                    embed.add_field(
                        name=f"**{hero['name']} ({hero['role']})**",
                        value=f"**Time Played:** {hero['timePlayed']}\n"
                              f"**Matches Played:** {hero['matchesPlayed']}\n"
                              f"**Wins:** {hero['wins']} ({hero['winPercentage']})\n"
                              f"**Kills/Deaths/Assists:** {hero['kills']}/{hero['deaths']}/{hero['assists']}\n"
                              f"**KDA:** {hero['kda']}\n"
                              f"**Total Damage:** {hero['totalDamage']}\n"
                              f"**Total Heals:** {hero['totalHeals']}\n"
                              "───────────────────────",
                        inline=False
                    )
                    embed.set_thumbnail(url=hero["imageUrl"])
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(f"No heroes found for {username}.")
        except Exception as e:
            await message.channel.send(f"An error occurred: {e}")

    if message.content.startswith('$leaderboard'):
        try:
            # Example leaderboard usernames (can be customized by users locally)
            usernames = [
                "example1",
                "example2",
                "example3",
                "example4",
                "example5",
                "example6"
            ]

            await message.channel.send(f"Fetching leaderboard data for {len(usernames)} players, please wait...")

            def get_player_data(username):
                return fetch_player_stats(username)

            with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                futures = {executor.submit(get_player_data, username): username for username in usernames}
                leaderboard = []
                for future in concurrent.futures.as_completed(futures):
                    player_data = future.result()
                    if player_data:
                        leaderboard.append({
                            "username": player_data["platformUser"],
                            "currentRank": player_data["currentRank"],
                            "currentRankScore": int(player_data["currentRankScore"].replace(",", "")) if player_data["currentRankScore"] != "N/A" else 0,
                            "avatarUrl": player_data["avatarUrl"]
                        })

            leaderboard = sorted(leaderboard, key=lambda x: x["currentRankScore"], reverse=True)

            embed = discord.Embed(title="Leaderboard (Highest Rank by SR)", color=0xFFD700)
            for i, player in enumerate(leaderboard, start=1):
                embed.add_field(
                    name=f"#{i} - {player['username']}",
                    value=f"**Rank:** {player['currentRank']}\n**SR:** {player['currentRankScore']}",
                    inline=False
                )
            embed.set_footer(text="Data powered by tracker.gg")
            embed.set_thumbnail(url=leaderboard[0]["avatarUrl"])
            await message.channel.send(embed=embed)

        except Exception as e:
            await message.channel.send(f"An error occurred: {e}")

    if message.content.startswith('$help'):
        try:
            embed = discord.Embed(
                title="Help - Available Commands",
                description="Here is a list of commands you can use with this bot:",
                color=0x1ABC9C
            )
            embed.add_field(
                name="$stats <username>",
                value="Displays the player's stats, including rank, KDA, and more.",
                inline=False
            )
            embed.add_field(
                name="$history <number_of_matches> <username>",
                value="Displays the match history of a player for the specified number of matches.",
                inline=False
            )
            embed.add_field(
                name="$top5 <username>",
                value="Shows the top 5 most played heroes for a player, including detailed stats for each hero.",
                inline=False
            )
            embed.add_field(
                name="$leaderboard",
                value="Displays a sample leaderboard (customize usernames locally).",
                inline=False
            )
            embed.add_field(
                name="$help",
                value="Displays this help message with a list of available commands.",
                inline=False
            )
            embed.set_footer(text="For any issues, contact the bot developer.")
            await message.channel.send(embed=embed)
        except Exception as e:
            await message.channel.send(f"An error occurred: {e}")

# Run the bot
try:
    # Load token from environment variable
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise ValueError("No DISCORD_BOT_TOKEN found in environment variables. Please set it before running the bot.")
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests.")
    else:
        raise e
except ValueError as e:
    print(e)