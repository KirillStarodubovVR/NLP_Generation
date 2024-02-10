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
    titles = soup.find_all('p')

    # names for series
    series_names = []
    # Extract text from elements
    for title in titles:
        a = title.find('a')

        path = a.get("href")

        test = path.split(" - ")

        series_names.append(
            "https://imsdb.com/transcripts/South-Park-" + test[1].replace(" ", "-").replace("-Script.", "."))

    return series_names


def get_text_from_html(url):
    # Download HTML content
    response = requests.get(url)
    html_content = response.text

    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    transcript = soup.find('pre')
    test_str = transcript.get_text(separator='\r', strip=False)
    transcript_list = test_str.split("\n")

    final_list = []
    for ind in range(1, len(transcript_list) - 1):
        pre_line = transcript_list[ind - 1].strip()
        cur_line = transcript_list[ind].strip()
        next_line = transcript_list[ind + 1].strip()
        if sum([bool(pre_line), bool(cur_line), bool(next_line)]) == 1:
            continue
        else:
            final_list.append(cur_line)

    new_name = url.split("/")[-1].replace(".html", ".txt").replace("-", "_")

    with open(os.path.join("raw_scripts", new_name), 'w', encoding='utf-8') as file:
        for line in final_list:
            file.write(line + "\n")

    return final_list


def clean_and_write_text(data, path):
    char = []
    texts = []
    flag = None

    for ind in range(1, len(data) - 1):

        prev_line = data[ind - 1]
        line = data[ind]
        next_line = data[ind + 1]

        if not line:
            continue

        elif line.isupper() and not prev_line and next_line:
            line = re.sub(r'\([^)]*\)', '', line)
            char.append(line)
            flag = "char"

        elif flag == "char" and line:
            text = line
            flag = "text"
            if not next_line:
                texts.append(text)
                flag = None

        elif flag == "text" and line:
            text += " " + line
            flag = "text"
            if not next_line:
                texts.append(text)
                flag = None

    new_name = path.split("/")[-1].replace(".html", ".txt").replace("-", "_")

    with open(os.path.join("preprocessed_scripts", new_name), 'w', encoding='utf-8') as file:
        for c, d in zip(char, texts):
            file.write(f"{c}: {d}\n")
