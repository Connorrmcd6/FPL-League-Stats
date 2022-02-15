This Repo will provide some interesting stats on your FPL mini leagues, such has who took the most hits, who is the most consistent etc... You can choose to run the summary manually or have it sent to you on telegram.

Set-Up:
- Clone the repo
- Make a copy of "example_configs.py" and name it "configs.py"
- To get your league_id, visit https://fantasy.premierleague.com/leagues on your desktop and click on the leage you want to use
- Once you click on the preferred league, your URL will look something like https://fantasy.premierleague.com/leagues/{league_id}/standings/c
- copy the league_id from the url and assign it to the league_id variable in the configs.py file

Manual Mode:
if you wish to run the script without telegram, you can now run all in the summary_manual.ipynb file. The stats and plots will be printed out below each cell.

Telegram:
- Download Telegram and start a chat with @BotFather, send "/newbot" and follow the prompts to create your own bot
- Save the API token as telegram_api_key in the configs.py file
- To get chat_id, start a chat with @userinfobot and send it "/start" then save the ID as chat_id in the configs.py file
- Send a message (eg. 'hello world!') to your bot to give it permission to send messages to your chat ID. 
- Run summary_telegram.ipynb

***IMPORTANT: Since this script will run through every one in your league it is advised not to use it on public or very large private leagues. Try and only use it for leagues with less than 25 members.***
