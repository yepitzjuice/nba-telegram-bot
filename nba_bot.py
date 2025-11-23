import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")

def get_odds():
    url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?regions=us&markets=h2h,spreads,totals&apiKey={ODDS_API_KEY}"
    return requests.get(url).json()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏀 Welcome to the NBA Odds Bot!\nType /games to see today's odds.")

async def games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    odds = get_odds()
    msg = "📅 NBA Games Today:\n\n"

    for g in odds:
        home = g["home_team"]
        away = g["away_team"]
        msg += f"{away} vs {home}\n"

    await update.message.reply_text(msg)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("games", games))
    print("Bot running on Render")
    app.run_polling()

if __name__ == "__main__":
    main()
