"""parsing script of the movie"""
import pandas as pd
import numpy as np
import nltk
import re
import os


def parse_scripts(path):
    """function take script.txt from dir and remove all strings except dialogs"""
    characters = []
    dialogs = []

    new_name = "prep" + "_" + path

    with open(os.path.join("raw_scripts", path), 'r') as file:
        lines = file.readlines()

    dialog = ""
    prev_line = "empty"
    pattern = r'^\d+\.?$'

    for idx, line in enumerate(lines):
        line = line.strip()

        if "INT." in line or "EXT." in line or "FADE" in line or "ACT" in line or "-" in line or "CUT TO" in line:
            # prev_line = "empty"
            continue

        elif line.isupper() and prev_line == "empty":
            line = re.sub(r'\([^)]*\)', '', line)
            characters.append(line.strip())
            prev_line = "char"

        elif prev_line == "char" and not line == "":
            dialog = line.strip()
            prev_line = "dialog"

        elif prev_line == "dialog" and not line == "":
            dialog += " " + line

        elif line == "" and prev_line == "dialog":
            dialog = re.sub(r'\([^)]*\)', '', dialog)
            dialog = dialog.replace("--", " ")
            dialogs.append(dialog)
            prev_line = "empty"

    # print(set(characters))
    # print(len(characters), len(dialogs))

    with open(os.path.join("preprocessed_scripts", new_name), 'w') as file:
        for c, d in zip(characters, dialogs):
            file.write(f"{c}: {d}\n")


def df_scripts(path):
    """function take preprocessed_script.txt from dir and create dataframes"""
    chars = []
    texts = []

    with open(os.path.join("preprocessed_scripts", path), 'r') as file:
        for line in file:
            char, text = line.split(":", 1)
            chars.append(char)
            texts.append(text.strip().lower())

    df_name = path.replace("prep_SP_", "df_").replace(".txt", ".csv")
    df = pd.DataFrame({'Characters': chars, 'Dialogs': texts})
    df.to_csv(os.path.join("dataframes", "south_park", df_name), index=False)


def collect_df():
    """function concatenate dataframes in one single dataframe"""
    dfs = []
    for file in os.listdir("dataframes/south_park"):
        dfs.append(pd.read_csv(os.path.join("dataframes", "south_park", file)))
    df = pd.concat(dfs, ignore_index=True)
    print(df["Characters"].value_counts()[:5])
    print(df["Characters"].unique())
    return df


def form_df(df, char):
    # get indices where character is CARTMAN
    cartman_df = df[df.Characters == char].dropna()
    cartman_ind = cartman_df.index.tolist()

    # get indices where speech could be to CARTMAN
    dialog_ind = (np.array(cartman_ind) - 1).tolist()

    # form datasets with CARTMAN's dialogs and possible dialogs to CARTMAN
    cartman_dialog = df.iloc[cartman_ind]
    text_to_cartman = df.iloc[dialog_ind].dropna(subset=["Dialogs"])
    # remove from text to cartman rows where speak Cartman
    text_to_cartman = text_to_cartman[text_to_cartman["Characters"] != char]

    # save data for debugging. Uncomment if necessary
    # cartman_dialog.to_csv("test_cartman.csv", index=cartman_ind)
    # text_to_cartman.to_csv("test_question.csv", index=dialog_ind)

    # find in dialog_to_cartman lines with char "?"
    mask = text_to_cartman['Dialogs'].str.contains('\?')

    questions_to_cartman = text_to_cartman[mask]
    # save data for debugging. Uncomment if necessary
    # questions_to_cartman.to_csv("questions_to_cartman.csv")

    questions_ind = questions_to_cartman.index.tolist()
    true_answers_ind = (np.array(questions_ind) + 1).tolist()
    cartman_answers = cartman_dialog.loc[true_answers_ind]

    # save data for debugging. Uncomment if necessary
    # cartman_answers.to_csv("cartman_answers.csv")

    # change name of columns for final dataframe
    questions_to_cartman = questions_to_cartman.rename(columns={"Characters": "questioner", "Dialogs": "question"})
    cartman_answers = cartman_answers.rename(columns={"Characters": char, "Dialogs": "answer"})

    questions_to_cartman.reset_index(inplace=True, drop=True)
    cartman_answers.reset_index(inplace=True, drop=True)

    df = pd.concat([questions_to_cartman, cartman_answers], axis=1)

    return df


def text_normalization(text):
    text = str(text).lower()  # convert to all lower letters
    spl_char_text = re.sub(r'[^a-z]', ' ', text)  # remove any special characters including numbers
    tokens = nltk.word_tokenize(spl_char_text)  # tokenize words
    lema = nltk.stem.wordnet.WordNetLemmatizer()  # lemmatizer initiation
    tags_list = nltk.pos_tag(tokens, tagset=None)  # parts of speech
    lema_words = []
    for token, pos_token in tags_list:
        if pos_token.startswith('V'):  # if the tag from tag_list is a verb, assign 'v' to it's pos_val
            pos_val = 'v'
        elif pos_token.startswith('J'):  # adjective
            pos_val = 'a'
        elif pos_token.startswith('R'):  # adverb
            pos_val = 'r'
        else:  # otherwise it must be a noun
            pos_val = 'n'
        lema_token = lema.lemmatize(token, pos_val)  # performing lemmatization
        lema_words.append(lema_token)  # addid the lemmatized words into our list
    return " ".join(lema_words)  # return our list as a human sentence
