import sys, os
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from abc_api_base import APIBase
BASEURL = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds"
load_dotenv()
API_KEY = os.getenv("NFL_ODDS_API_KEY")

class NFL_API(APIBase):
    def call_api(self):
        return self.get_api()

    def __str__(self, all_team_odds):
        print(f'Best odds for {all_team_odds["team"]}: is {all_team_odds["price"]} at {all_team_odds["bookmaker"]} for the game {all_team_odds["game"]}')

def find_best_odds(selected_team, data):
    all_team_odds = []
    for game in data:
        if selected_team.lower() == game['home_team'].lower() or selected_team.lower() == game["away_team"].lower():
            date_of_soonest_game = game['commence_time']
            break
    for game in data:
        if selected_team.lower() == game['home_team'].lower() or selected_team.lower() == game["away_team"].lower():
            for bookmaker in game['bookmakers']:
                for market in bookmaker['markets']:
                    if market['key'] == 'h2h':
                        outcomes = market['outcomes']
                        for outcome in outcomes:
                            if game["commence_time"] == date_of_soonest_game and outcome['name'].lower() == selected_team.lower():
                                all_team_odds.append({
                                    "bookmaker": bookmaker['title'],
                                    "price": outcome['price'],
                                    "team": outcome['name'],
                                    "game": f"{game['home_team']} vs {game['away_team']}"
                                })
    all_team_odds.sort(key=lambda x: x['price'], reverse=True)
    return all_team_odds

def take_mascot_or_state(selected_team):
    if selected_team.lower() == "chicago" or selected_team == "bears":
        selected_team = "Chicago Bears"
    if selected_team.lower() == "giants":
        selected_team = "New York Giants"
    if selected_team.lower() == "jets":
        selected_team = "New York Jets"
    if selected_team.lower() == "washington" or selected_team == "football team":
        selected_team = "Washington Football Team"
    if selected_team.lower() == "las vegas" or selected_team == "raiders":
        selected_team = "Las Vegas Raiders"
    if selected_team.lower() == "chargers":
        selected_team = "Los Angeles Chargers"
    if selected_team.lower()  == "rams":
        selected_team = "Los Angeles Rams"
    if selected_team.lower() == "tennessee" or selected_team == "titans":
        selected_team = "Tennessee Titans"
    if selected_team.lower() == "new england" or selected_team == "patriots":
        selected_team = "New England Patriots"
    if selected_team.lower() == "san francisco" or selected_team == "49ers":
        selected_team = "San Francisco 49ers"
    if selected_team.lower() == "miami" or selected_team == "dolphins":
        selected_team = "Miami Dolphins"
    if selected_team.lower() == "green bay" or selected_team == "packers":
        selected_team = "Green Bay Packers"
    if selected_team.lower() == "arizona" or selected_team == "cardinals":
        selected_team = "Arizona Cardinals"
    if selected_team.lower() == "pittsburgh" or selected_team == "steelers":
        selected_team = "Pittsburgh Steelers"    
    if selected_team.lower() == "jacksonville" or selected_team == "jaguars":
        selected_team = "Jacksonville Jaguars"
    if selected_team.lower() == "cleveland" or selected_team == "browns":
        selected_team = "Cleveland Browns"
    if selected_team.lower() == "buffalo" or selected_team == "bills":
        selected_team = "Buffalo Bills"
    if selected_team.lower() == "new orleans" or selected_team == "saints":
        selected_team = "New Orleans Saints"
    if selected_team.lower() == "seattle" or selected_team == "seahawks":
        selected_team = "Seattle Seahawks"
    if selected_team.lower() == "indianapolis" or selected_team == "colts":
        selected_team = "Indianapolis Colts"
    if selected_team.lower() == "houston" or selected_team == "texans":
        selected_team = "Houston Texans"
    if selected_team.lower() == "atlanta" or selected_team == "falcons":
        selected_team = "Atlanta Falcons"
    if selected_team.lower() == "detroit" or selected_team == "lions":
        selected_team = "Detroit Lions"
    if selected_team.lower() == "minnesota" or selected_team == "vikings":
        selected_team = "Minnesota Vikings"
    if selected_team.lower() == "carolina" or selected_team == "panthers":
        selected_team == "Carolina Panthers"
    if selected_team.lower() == "tampa bay" or selected_team == "buccaneers":
        selected_team = "Tampa Bay Buccaneers"
    if selected_team.lower() == "denver" or selected_team == "broncos":
        selected_team = "Denver Broncos"
    if selected_team.lower() == "kansas city" or selected_team == "chiefs":
        selected_team = "Kansas City Chiefs"
    if selected_team.lower() == "cincinnati" or selected_team == "bengals":
        selected_team = "Cincinnati Bengals"
    if selected_team.lower() == "philadelphia" or selected_team == "eagles":
        selected_team = "Philadelphia Eagles"
    if selected_team.lower() == "baltimore" or selected_team == "ravens":
        selected_team = "Baltimore Ravens"
    return selected_team

def list_upcoming_games(data):
    for game in data:
        print(f"{game['home_team']} vs {game['away_team']} at {game['commence_time']}")

def main():
    print(
        "Welcome to the NFL H2H Best Odds Finder!" 
        f"\nHere is a list of upcoming games: "
        )
    regions = "us"
    markets = "h2h"
    dateFormat = "iso"
    oddsFormat = "american"
    api = NFL_API(BASEURL, params={
                                   "apiKey": API_KEY, 
                                   "regions": regions,
                                   "markets": markets,
                                   "dateFormat": dateFormat,
                                   "oddsFormat": oddsFormat,}, 
                                   timeout=10)
    data = api.call_api()
    if data is None:
        print(f"API returned no data." 
              f"status={api.status}, message={api.message}")
    else:
        list_upcoming_games(data)

    selected_team = input(f"\nWhat team would you like to find the best odds for in their next game?: ")
    all_team_odds = find_best_odds(take_mascot_or_state(selected_team), data)
    api.__str__(all_team_odds[0])

main()