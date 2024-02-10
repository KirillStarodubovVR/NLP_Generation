import numpy as np
from collections import Counter
from math import log

class ToyTfIdf:
    def __init__(self, sentences):
        self.sentences = [self.preprocess(sentence) for sentence in sentences]
        self.tf_scores = []
        self.idf_scores = {}
        self.tf_idf_scores = []

    @staticmethod
    def preprocess(sentence: str) -> str:
        # Lowercase and remove punctuation
        return sentence.lower().replace('.', '')

    def compute_tf(self, sentence: str) -> dict[str, float]:
        tf_dict = {}
        words = sentence.split()
        word_count = len(words)
        word_counts = Counter(words)
        for word, count in word_counts.items():
            tf_dict[word] = count / float(word_count)
        return tf_dict

    def compute_idf(self):
        N = len(self.sentences)
        all_words = set(word for sentence in self.sentences for word in sentence.split())
        for word in all_words:
            count = sum(word in sentence.split() for sentence in self.sentences)
            if count == len(self.sentences):
                self.idf_scores[word] = 0
            else:
                self.idf_scores[word] = log(N / (1 + float(count)))

    def compute_tf_idf(self):
        for tf in self.tf_scores:
            tf_idf_dict = {}
            for word, tf_score in tf.items():
                tf_idf_dict[word] = tf_score * self.idf_scores[word]
            self.tf_idf_scores.append(tf_idf_dict)

    def calculate_scores(self) -> list[dict[str, float]]:
        # Calculate TF scores
        self.tf_scores = [self.compute_tf(sentence) for sentence in self.sentences]

        # Calculate IDF scores
        self.compute_idf()

        # Calculate TF-IDF scores
        self.compute_tf_idf()

        return self.tf_idf_scores


sentences = [
    "Кот спит на подушке",
    "Собака лежит на ковре в гостиной",
    "Кот и собака играют вместе на улице"
]

toy_tf_idf = ToyTfIdf(sentences)
tf_idf_results = toy_tf_idf.calculate_scores()
print(tf_idf_results)


toy_tf_idf = ToyTfIdf(["Кот спит на подушке"])
computed_tf = toy_tf_idf.compute_tf(toy_tf_idf.sentences[0])
expected_tf_for_word_кот = 0.25  # The word 'Кот' appears once in a sentence of 4 words.
assert computed_tf.get('кот', 0) == expected_tf_for_word_кот, "TF calculation is incorrect for word 'кот'"

toy_tf_idf = ToyTfIdf(["Кот спит", "Кот ест", "Кот играет"])
toy_tf_idf.compute_idf()
expected_idf_for_common_word = 0  # The word 'Кот' appears in all 3 documents.
assert toy_tf_idf.idf_scores.get('кот', -1) == expected_idf_for_common_word, "IDF calculation is incorrect for a word appearing in all documents"

toy_tf_idf = ToyTfIdf(["Кот спит на подушке", "Собака лежит", "Кот и собака играют"])
toy_tf_idf.tf_scores = [toy_tf_idf.compute_tf(sentence) for sentence in toy_tf_idf.sentences]
toy_tf_idf.compute_idf()
toy_tf_idf.compute_tf_idf()
expected_tf_idf_for_word_спит = toy_tf_idf.tf_scores[0]['спит'] * toy_tf_idf.idf_scores['спит']
assert toy_tf_idf.tf_idf_scores[0].get('спит', 0) == expected_tf_idf_for_word_спит, "TF-IDF calculation is incorrect for word 'спит'"

toy_tf_idf = ToyTfIdf(["Кот спит", "Собака лежит", "Кот играет"])
result = toy_tf_idf.calculate_scores()
assert len(result) == 3, "The number of calculated TF-IDF dictionaries should match the number of sentences"
assert all(isinstance(d, dict) for d in result), "Each item in the result should be a dictionary"

print("All checks passed!")