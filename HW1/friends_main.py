import requests
from bs4 import BeautifulSoup

import re
import os

from tqdm import tqdm
from parse_friends import get_transcripts_from_url, get_text_from_html, clean_and_write_text
from preprocess_for_friends import df_scripts, collect_df, form_df

raw_texts_exists = True  # change on False to download transcripts and preprocess them
# parse data from website to get txt transcripts
transcript_paths = get_transcripts_from_url("https://fangj.github.io/friends/")

# define list with certain scripts from south park
# dir_list = [file for file in os.listdir("./raw_scripts")]
if not raw_texts_exists:
    for path in tqdm(transcript_paths):
        transcript_name = get_text_from_html(path)
        clean_and_write_text(transcript_name)

dir_list = [file for file in os.listdir("./friends_preprocessed_scripts")]
#
for preprocessed_script in dir_list:
    df_scripts(preprocessed_script)

# concatenate data in one single dataframe
df = collect_df()

# form the final dataset for tf-idf / word2vec, which no need labels between strings
df = form_df(df, "ross")

# create final dataframe for tf-idf
df.to_csv("friends.csv", index=False)
print("file created")

