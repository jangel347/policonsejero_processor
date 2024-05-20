import pandas as pd
import string
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

class Classifier:
    def __init__(self, path):
        self.path = path
        self.vectorizer = None
        self.classifier = None
        self.train()

    def train(self):
        spam_or_ham = pd.read_csv(self.path, encoding='utf-8',sep=";")[["v1", "v2"]]
        spam_or_ham.columns = ["label", "text"]
        spam_or_ham.head()

        print(spam_or_ham["label"].value_counts())

        spam_or_ham.head()["text"].apply(self.tokenize)

        train_text, test_text, train_labels, test_labels = train_test_split(spam_or_ham["text"], spam_or_ham["label"], stratify=spam_or_ham["label"])
        print(f"Training examples: {len(train_text)}, testing examples {len(test_text)}")

        real_vectorizer = CountVectorizer(tokenizer = self.tokenize, binary=True)
        train_X = real_vectorizer.fit_transform(train_text)
        test_X = real_vectorizer.transform(test_text)

        classifier = LinearSVC()
        classifier.fit(train_X, train_labels)
        LinearSVC(C=1.0, class_weight=None, dual=True, fit_intercept=True,
                intercept_scaling=1, loss='squared_hinge', max_iter=1000,
                multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
                verbose=0)

        predicciones = classifier.predict(test_X)
        accuracy = accuracy_score(test_labels, predicciones)
        print(f"Accuracy: {accuracy}")

        self.classifier = classifier
        self.vectorizer = real_vectorizer
        print('REPORTE DE CLASIFICACIÓN PREDICCIONES: \n', classification_report(test_labels,predicciones))

    def generate_predict(self, frases):
        frases_X = self.vectorizer.transform(frases)
        predicciones = self.classifier.predict(frases_X)
        # print('REPORTE DE CLASIFICACIÓN: \n', classification_report(frases_X['label'],predicciones))
        for text,label in zip(frases, predicciones):
            return label

    def tokenize(self, sentence):
        punctuation = set(string.punctuation)
        tokens = []
        for token in sentence.split():
            new_token = []
            for character in token:
                if character not in punctuation:
                    new_token.append(character.lower())
            if new_token:
                tokens.append("".join(new_token))
        return tokens