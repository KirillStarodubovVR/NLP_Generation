import os
import bs4
import re
import pandas as pd
import numpy as np
import nltk
from tqdm import tqdm
from preprocess_for_south_park import parse_scripts, df_scripts, collect_df, form_df
from parse_transcripts_for_south_park import get_transcripts_from_url, get_text_from_html, clean_and_write_text

"""
Done! Congratulations on your new bot. You will find it at t.me/CartmanHW_bot. 
You can now add a description, about section and profile picture for your bot, 
see /help for a list of commands. By the way, when you've finished creating your 
cool bot, ping our Bot Support if you want a better username for it. Just make 
sure the bot is fully operational before you do this.

Use this token to access the HTTP API:
6840926389:AAHNUkJQKpbDQAqInbCN8SBLeol54FaDAbk
Keep your token secure and store it safely, it can be used by anyone to control your bot.

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
"""
raw_texts_exists = True # change on False to download transcripts and preprocess them
# parse data from website to get txt transcripts
# 'https://imsdb.com/TV/South%20Park.html' page from IMDBs website with transcripts
transcript_paths = get_transcripts_from_url('https://imsdb.com/TV/South%20Park.html')
print(transcript_paths)


# define list with certain scripts from south park
# dir_list = [file for file in os.listdir("./raw_scripts")]
if not raw_texts_exists:
    for path in tqdm(transcript_paths):
        raw_text = get_text_from_html(path)
        clean_and_write_text(raw_text, path)

# form pandas dataset from preprocessed scripts
# define list with certain scripts from south park
dir_list = [file for file in os.listdir("./preprocessed_scripts")]

for preprocessed_script in dir_list:
    df_scripts(preprocessed_script)

# concatenate data in one single dataframe
df = collect_df()

# form the final dataset for tf-idf / word2vec, which no need labels between strings
df = form_df(df, "CARTMAN")

# create final dataframe for tf-idf
df.to_csv("south_park.csv", index=False)
print("file created")

