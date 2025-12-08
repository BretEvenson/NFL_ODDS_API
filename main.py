import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys, os
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from abc_api_base import APIBase
BASEURL = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds"
load_dotenv()
API_KEY = os.getenv("NFL_ODDS_API_KEY")

root = tk.Tk()
root.configure(bg="#1e1e1e")
root.geometry("1000x1000")
root.title("NFL H2H Best Odds Finder")
img_path = os.path.join(os.path.dirname(__file__), "NFL.png")
bg_img = Image.open(img_path)
bg_photo = ImageTk.PhotoImage(bg_img)

background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

style = ttk.Style()
style.theme_use("clam")
style.configure("Small.TLabel", font=("Arial", 12), foreground="white", background="#1e1e1e")
style.configure("Medium.TLabel", font=("Arial", 14), foreground="white", background="#1e1e1e")
style.configure(
    "Confirm.TButton",
    font=("Arial", 16),
    foreground="white",
    background="#333333",
    bordercolor="#333333",
    darkcolor="#333333",
    lightcolor="#333333",
    focuscolor="#333333",
    highlightcolor="#333333"
)
style.map(
    "Confirm.TButton",
    background=[("active", "#444444"), ("!active", "#333333")],
    foreground=[("disabled", "#888888"), ("!disabled", "white")]
)
style.configure(
    "Team.TButton",
    font=("Arial", 12),
    foreground="white",
    background="#2a2a2a",
    bordercolor="#2a2a2a",
    darkcolor="#2a2a2a",
    lightcolor="#2a2a2a",
    focuscolor="#2a2a2a",
    highlightcolor="#2a2a2a",
    padding=4
)
style.map(
    "Team.TButton",
    background=[("active", "#3a3a3a"), ("!active", "#2a2a2a")],
    foreground=[("disabled", "#888888"), ("!disabled", "white")]
)

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
    label = ttk.Label(root, text="Upcoming NFL Games", style="Medium.TLabel")
    label.pack(pady=3)
    game_number = 1
    for game in data:
        button_frame = tk.Frame(root, bg="#1e1e1e")
        button_frame.columnconfigure({game_number}, weight=1)
        
        home_team = ttk.Button(button_frame, text=f"{game['home_team']}", style="Team.TButton")
        vs_label = ttk.Label(button_frame, text="vs", style="Small.TLabel")
        away_team = ttk.Button(button_frame, text=f"{game['away_team']}", style="Team.TButton")


        home_team.bind("<Button-1>", get_selected_team)
        away_team.bind("<Button-1>", get_selected_team)

        home_team.grid(row=game_number, column=1, sticky=tk.W+tk.E, padx=5, pady=2)
        vs_label.grid(row=game_number, column=2, padx=5, pady=2)
        away_team.grid(row=game_number, column=3, sticky=tk.W+tk.E, padx=5, pady=2)
        button_frame.pack(pady=3)
        game_number += 1
    confirm_button = ttk.Button(root, text="Confirm Selection", style="Confirm.TButton", command=confirm_button_function, width=20)
    confirm_button.pack(pady=10)

current_selection_label = ttk.Label(root, text="Selected Team: NONE", style="Small.TLabel")
current_selection_label.pack(pady=2)

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
            result_label = ttk.Label(root, text="", style="Medium.TLabel")
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
        if widget is not background_label:
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