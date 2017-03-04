read -p "commit description: " description
cd Desktop/DiscordBot/BeepBoopBot/BeepBoopBot
git add .
git commit -m description
git push origin master
read -p "waiting"