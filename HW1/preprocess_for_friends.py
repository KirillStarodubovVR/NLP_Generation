"""parsing script of the movie"""
import pandas as pd
import numpy as np
import random
import nltk
import re
import os


def df_scripts(path):
    """function take preprocessed_script.txt from dir and create dataframes"""
    chars = []
    texts = []

    with open(os.path.join("friends_preprocessed_scripts", path), 'r', encoding="utf-8") as file:
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
    df = pd.concat(dfs, ignore_index=True).dropna().reset_index(drop=True)
    # find characters with more than 10 texts
    high_chars = df.Characters.value_counts()
    high_chars_ind = high_chars[high_chars > 10].index
    df = df[df["Characters"].isin(high_chars_ind)]
    # optional function to clean dialogs
    print(f"Number of characters in dataframe {len(df.Characters.value_counts())}")
    return df


def form_df(df, char):
    # get indices where character is favorite_character
    favorite_character_df = df[df.Characters == char]  # .dropna()
    favorite_character_ind = favorite_character_df.index.tolist()

    # get indices where speech could be to favorite charecter
    text_to_favorite_character_ind = (np.array(favorite_character_ind) - 1).tolist()

    # form datasets with favorite charecter's dialogs and possible dialogs to favorite charecter
    # favorite_character_dialog = df.iloc[favorite_character_ind] restore
    favorite_character_dialog = df[df.index.isin(favorite_character_ind)]
    # text_to_favorite_character = df.iloc[text_to_favorite_character_ind]  restore# .dropna(subset=["Dialogs"])
    text_to_favorite_character = df[df.index.isin(text_to_favorite_character_ind)]
    # remove from text to cartman rows where speak Cartman
    text_to_favorite_character = text_to_favorite_character[text_to_favorite_character["Characters"] != char]

    # save data for debugging. Uncomment if necessary
    # favorite_character_dialog.to_csv("test_favotite.csv", index=favorite_character_ind)
    # text_to_favorite_character.to_csv("test_question.csv", index=text_to_favorite_character_ind)

    # find in dialog_to_cartman lines with char "?"
    # mask = text_to_favorite_character['Dialogs'].str.contains('\?')
    # question_to_favorite_character = text_to_favorite_character[mask]
    # if we want to get all texts to our favorite actor, then we leave text_to_favorite_character
    question_to_favorite_character = text_to_favorite_character

    # save data for debugging. Uncomment if necessary
    # question_to_favorite_character.to_csv("question_to_favorite_character.csv")

    question_to_favorite_character_ind = question_to_favorite_character.index.tolist()
    true_answers_ind = (np.array(question_to_favorite_character_ind) + 1).tolist()
    # favorite_character_answer = favorite_character_dialog.loc[true_answers_ind]
    favorite_character_answer = favorite_character_dialog[favorite_character_dialog.index.isin(true_answers_ind)]
    # save data for debugging. Uncomment if necessary
    favorite_character_answer.to_csv("favorite_character_answer.csv")

    # change name of columns for final dataframe
    question_to_favorite_character = question_to_favorite_character.rename(
        columns={"Characters": "questioner", "Dialogs": "question"})
    favorite_character_answer = favorite_character_answer.rename(columns={"Characters": "answerer", "Dialogs": "answer"}) # char or answerer !!!!!!

    question_to_favorite_character.reset_index(inplace=True, drop=True)
    favorite_character_answer.reset_index(inplace=True, drop=True)

    df = pd.concat([question_to_favorite_character, favorite_character_answer], axis=1)

    return df


def form_df_negative(df, df_char, char):
    # get from form_df true data, but without labels. At this step define label = 1 for all sentences
    true_label = pd.DataFrame({"label": np.ones(shape=len(df_char), dtype=np.int8)})
    # add from the right side new columns with labels
    df_true_labels = pd.concat([df_char, true_label], axis=1)


    # find text for this random_character and without questions
    # favorite_character_df = df[df.Characters == random_char].str.contains('\?')
    random_character_df = df[df.Characters != char].reset_index(drop=True)

    indices = np.random.choice(np.arange(len(random_character_df)), size=(len(df_true_labels)), replace=False)
    random_character_df = random_character_df[random_character_df.index.isin(indices)]
    df_negative_labels = df_true_labels.drop(columns="label", axis=1)
    df_negative_labels["answer"] = random_character_df["Dialogs"].reset_index(drop=True)
    df_negative_labels = df_negative_labels.rename(columns={"Dialogs": "question"})

    negative_label = pd.DataFrame({"label": np.zeros(shape=len(df_char), dtype=np.int8)})
    df_negative_labels = pd.concat([df_negative_labels, negative_label], axis=1)

    # fincal concatenation of dataframes with true and negative labels
    final_df = pd.concat([df_negative_labels, df_true_labels], axis=0)


    # How to shuffle data in pandas dataframe
    final_df = final_df.sample(frac=1).reset_index(drop=True)

    return final_df

