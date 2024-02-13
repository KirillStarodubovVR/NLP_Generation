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
    transcript_paths = []
    # Extract text from elements
    for title in titles:
        a = title.find('a')

        path = a.get("href")

        transcript_paths.append("https://fangj.github.io/friends/" + path)

    return transcript_paths


def get_text_from_html(url):
    path = url
    response = requests.get(path)
    html_content = response.text

    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    transcript = soup.find_all('p')

    txt_name = path.split("/")[-1].replace(".html", ".txt")

    final_transcript = []

    with open(os.path.join("friends_raw_scripts", txt_name), 'w', encoding='utf-8') as file:
        for t in transcript:
            line = t.get_text(strip=False)
            line = line.replace('"', "'").replace("\n", " ")
            file.write(line + "\n")
            final_transcript.append(line)

    return final_transcript


def clean_and_write_text(data, path):
    char = []
    texts = []
    flag = None
    pattern = re.compile(r'\b\w+:')

    for ind in range(0, len(data) - 1):

        line = data[ind].lower()
        line = re.sub(r"\([^()]*\)|\[[^\[\]]*\]", '', line)
        line = line.strip().replace("\n", " ")

        next_line = data[ind + 1].lower()
        next_line = re.sub(r"\([^()]*\)|\[[^\[\]]*\]", '', next_line).strip()

        if next_line in ["commercial break", "closing credits", "opening credits", "end"]:
            next_line = ""

        if "written by:" in line or not line or "opening credits" in line or line in ["commercial break",
                                                                                      "closing credits",
                                                                                      "opening credits"]:
            continue

        elif pattern.search(line):
            name, text = line.split(":", maxsplit=1)
            char.append(name)
            text = re.sub(r'\([^)]*\)', '', text)
            text = text.strip()

            if pattern.search(next_line) or not next_line:
                texts.append(text)

        elif line:
            text += " " + line
            if pattern.search(next_line) or not next_line:
                texts.append(text)

        # if len(char) != len(texts):
        #     print(line)
        #     print(ind)

    txt_name = path.split("/")[-1].replace(".html", ".txt")
    new_name = "pre_" + txt_name
    with open(os.path.join("friends_preprocessed_scripts", new_name), 'w', encoding='utf-8') as file:
        for c, d in zip(char, texts):
            file.write(f"{c}: {d}\n")
