import requests
from bs4 import BeautifulSoup

import re
import os


def get_transcripts_from_url(url):
    # Send a GET request to the URL and retrieve the webpage content
    response = requests.get(url)

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find elements by tag name
    titles = soup.find_all('li')

    # names for series
    series_names = []
    # Extract text from elements
    for title in titles:
        a = title.find('a')

        path = a.get("href")

        series_names.append("https://fangj.github.io/friends/" + path)

    return series_names


transcript_paths = get_transcripts_from_url('https://fangj.github.io/friends/')

# for path in transcript_paths[1]:
path = transcript_paths[30]
print(path)
response = requests.get(path)
html_content = response.text

# Parse HTML content
soup = BeautifulSoup(html_content, 'html.parser')

transcript = soup.find_all('p')

txt_name = path.split("/")[-1].replace(".html", ".txt")

with open(os.path.join("friends_raw_scripts", txt_name), 'w', encoding='utf-8') as file:
    text = soup.get_text(strip=False).lower()
    file.write(text + "\n")

char = []
texts = []
flag = None
pattern = re.compile(r'\b\w+:')

with open(os.path.join("friends_raw_scripts", txt_name), 'r', encoding='utf-8') as file:
    final_transcript = file.readlines()

skip_lines = 10
pattern = re.compile(r'\b\w+:')
scene_words = ["commercial break", "closing credits", "opening credits", "end"]
for ind in range(1, len(final_transcript) - 1):
    final_list = []

    pre_line = final_transcript[ind - 1].strip()
    cur_line = final_transcript[ind].strip()
    next_line = final_transcript[ind + 1].strip()

    next_condition = re.sub(r"\([^()]*\)|\[[^\[\]]*\]", '', next_line).strip()
    cur_conditon = re.sub(r"\([^()]*\)|\[[^\[\]]*\]", '', cur_line).strip()

    if sum([bool(pre_line), bool(cur_line), bool(next_line)]) == 1:
        continue

    elif cur_line in scene_words:
        continue

    elif "by:" in cur_line or "note:" in cur_line:
        continue

    elif "[" in cur_line or "]" in cur_line:
        continue

    elif not cur_conditon:
        continue

    elif pattern.search(cur_line) and flag == None:
        name, text = cur_line.split(":", maxsplit=1)
        char.append(name)
        text = re.sub(r'\([^)]*\)', '', text)
        text = text.strip()
        flag = "char"

        if pattern.search(next_line) or not next_condition or next_line in scene_words or "[" in next_line:
            texts.append(text)
            flag = None

            if len(char) != len(texts):
                print(ind)
                print(char[-1], texts[-1])

    elif cur_line and flag == 'char':
        text += " " + cur_line
        if pattern.search(next_line) or not next_condition or next_line in scene_words or "[" in next_line:
            text = re.sub(r"\([^()]*\)|\[[^\[\]]*\]", '', text).strip()
            texts.append(text)
            flag = None

            if len(char) != len(texts):
                print(ind)
                print(char[-1], texts[-1])

txt_name = path.split("/")[-1].replace(".html", ".txt")
new_name = "pre_" + txt_name
with open(os.path.join("friends_preprocessed_scripts", new_name), 'w', encoding='utf-8') as file:
    for c, d in zip(char, texts):
        file.write(f"{c}: {d}\n")

print("script finished")
