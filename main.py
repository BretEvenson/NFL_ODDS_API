import tkinter as tk
import sys, os
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from abc_api_base import APIBase
BASEURL = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds"
load_dotenv()
API_KEY = os.getenv("NFL_ODDS_API_KEY")

root = tk.Tk()
root.geometry("1000x1000")
root.title("NFL H2H Best Odds Finder")
selected_team_var = tk.StringVar(value="")

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

def list_upcoming_games(data):
    label = tk.Label(root, text="Upcoming NFL Games", font=("Arial", 16))
    label.pack(pady=10)
    game_number = 1
    for game in data:
        button_frame = tk.Frame(root)
        button_frame.columnconfigure({game_number}, weight=1)
        
        home_team = tk.Button(button_frame, text=f"{game['home_team']}")
        vs_label = tk.Label(button_frame, text="vs")
        away_team = tk.Button(button_frame, text=f"{game['away_team']}")

        home_team.bind("<Button-1>", get_selected_team)
        away_team.bind("<Button-1>", get_selected_team)

        home_team.grid(row=game_number, column=1, sticky=tk.W+tk.E, padx=5, pady=2)
        vs_label.grid(row=game_number, column=2, padx=5, pady=2)
        away_team.grid(row=game_number, column=3, sticky=tk.W+tk.E, padx=5, pady=2)
        button_frame.pack(pady=5)
        game_number += 1
    confirm_button = tk.Button(root, text="Confirm Selection", font=("Arial", 20) , command=confirm_button_function)
    confirm_button.pack(pady=10)

current_selection_label = tk.Label(root, text="Selected Team: NONE", font=("Arial", 14))
current_selection_label.pack(pady=10)

def get_selected_team(event):
    clicked_button = event.widget
    team = clicked_button["text"]
    current_selection_label.config(text=f"Selected Team: {team}")
    selected_team_var.set(team)

def confirm_button_function():
    clear_frame()
    team = selected_team_var.get()
    if team:
        all_team_odds = find_best_odds(team, data)  # make sure 'data' is accessible here
        if all_team_odds:
            result_label = tk.Label(root, text="", font=("Arial", 16))
            result_label.pack(pady=10)
            if all_team_odds[0]["price"] > 0:
                result_label.config(
                    text=f"Best odds for {all_team_odds[0]['team']}: "
                        f"+{all_team_odds[0]['price']} at {all_team_odds[0]['bookmaker']} "
                        f"for the game {all_team_odds[0]['game']}"
                )
            else:
                result_label.config(
                    text=f"Best odds for {all_team_odds[0]['team']}: "
                        f"{all_team_odds[0]['price']} at {all_team_odds[0]['bookmaker']} "
                        f"for the game {all_team_odds[0]['game']}"
                )
        else:
            result_label.config(text=f"No odds found for {team}")
    
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

def main():
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
    global data
    data = api.call_api()
    if data is None:
        print(f"API returned no data." 
              f"status={api.status}, message={api.message}")
    else:
        list_upcoming_games(data)
        root.mainloop()
    
    

main()