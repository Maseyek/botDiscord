This bot was created for the ultimate Los 40 Classic radio experience! Plug it into a voice channel, hit play, and enjoy seamless streaming for you and your friends.

It's easy to alter and extend to work with other radio stations, and I plan to expand it with more features in the future.

Features:
- Play Los 40 Classic (or any other radio station with a simple URL modification).
- Join and leave voice channels automatically.
- Respond to basic commands like !los40, !leave

Commands\
!los40: Makes the bot join the voice channel the user is in and starts blasting Los 40 Classic.\
!leave: Makes the bot leave the voice channel.

Deployment Guide (Fresh install):\
To deploy the bot on any Linux-based VM (Ubuntu recommended), follow these steps:

1) Update package list\
sudo apt update
2) Install Python 3.10\
sudo apt install python3

3) Install pip (Python package manager)\
sudo apt install python3-pip

4) Install system dependencies\
sudo apt install ffmpeg\
sudo apt install libpq-dev

5) Clone repository\
git clone https://github.com/Maseyek/botDiscord.git

6) Change to the repository directory\
cd botDiscord

7) Install required libraries\
pip3 install -r /path/to/your-repo/requirements.txt

8) Set up your environment variables\
a) Create .env file\
nano .env'\
b) Add token\
BOT_TOKEN=YOUR_BOT_TOKEN

9) Run the Bot\
python3 bot.py
