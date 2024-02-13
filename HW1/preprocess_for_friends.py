"""parsing script of the movie"""
import pandas as pd
import numpy as np
import nltk
import re
import os


def df_scripts(path):
    """function take preprocessed_script.txt from dir and create dataframes"""
    chars = []
    texts = []

    with open(os.path.join("friends_preprocessed_scripts", path), 'r') as file:
        for line in file:
            char, text = line.split(":", 1)
            chars.append(char)
            texts.append(text.strip().lower())

    df_name = path.replace("prep_SP_", "df_").replace(".txt", ".csv")
    df = pd.DataFrame({'Characters': chars, 'Dialogs': texts})
    df.to_csv(os.path.join("dataframes", "friends", df_name), index=False)


def collect_df():
    """function concatenate dataframes in one single dataframe"""
    dfs = []
    for file in os.listdir("dataframes/friends"):
        dfs.append(pd.read_csv(os.path.join("dataframes", "friends", file)))
    df = pd.concat(dfs, ignore_index=True)
    print(df["Characters"].value_counts()[:10])
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
