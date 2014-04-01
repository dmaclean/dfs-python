dfs-python
==========
This project is an attempt at automating data gathering, projection generation, and lineup generation for DFS league.  At this point, the only supported sport is NBA and data gathering and projection generation are underway.  Lineup generation needs to be ported from a separate project.


Data gathering
==============
Data gathering is accomplished with the basketball.py script.  It works with the following switches:
source=<file-name|site> - This specifies where the input is coming from (HTML is expected, regardless of the source).  When a valid HTML file is named, the file is read in and parsed, but no database interaction occurs.  This is basically a test mode.
When "site" is specified, the input source is basketball-reference.com.

season=<year> - This tells the script we are only interested in the specified season.  It's used when scraping game logs and season data.

type=<teams|schedule|players> - When "teams" is specified for type, only team-related data is retrieved.  When "schedule" is specified, it retrieves the schedules for all teams.  When "players" is specified (or nothing is specified- players is default) then all player-related data (game logs, season-long data, etc.) is retrieved.

all_players=<true|false> - True indicates that all players, retired and active, are retrieved.  False indicates we only are interested in active players.  Use false for nightly scrapes and true for grabbing all data.

yesterday_only=<true|false> - True indicates that we should consult the current year's schedule and only grab data of players who played the previous night.  False indicates that we're scraping all players.  This, coupled with season and all_players can be used to quickly only scrape data from the previous night.

Make sure that basketball.sql is run prior to running this script, otherwise there will be nowhere for the scraped data to go.

Projection generation
===================
The projections.py script is used for generating projections based on the data that's available in the database.  It works with the following switches:
regression=<true|false> - True indicates that we want to run regression testing for a particular season (defaults to 2013 - hardcoded currently so this needs work) and dump the results, along with MSE to regression.csv.  False indicates that we want projections for the current day's games.

Currently, the script uses pace and DvP to adjust season averages for stats that factor into fantasy points for each player.  From there, the FantasyPointCalculator class is given a map of these values and calculates how many FPs they're worth.  This becomes the projection, which is added to a CSV of projections (one CSV per site), along with the other players.
The CSV will contain several columns, including:
- player
- position (site specific)
- projection
- salary
- floor (based on standard deviation)
- consistency factor
- ceiling (based on standard deviation)
- vegas odds
- DvP ranking of opponent
- Dollars-per-point

One last component worth mentioning is how injuries are managed.  Currently, there's an injury table that contains all injuries (or, more generally, missed games) for each player.  This can be populated daily with SQL inserts after monitoring injury reports or with a tool in the InjuryManager class, which analyzes the game logs in the game_totals_basic table and games played in the team_game_totals table to determine which games a player has missed.  The former is helpful for current projections so we can attempt to redistribute minutes to active players.  The latter is helpful for regression testing.

Lineup generation
================
Coming soon.  This needs to be ported from a Groovy application.
