import re
import string
from collections import Counter
from spacy.matcher import PhraseMatcher
from spacy.lang.es.stop_words import STOP_WORDS
import torch
import transformers
transformers.logging.set_verbosity_error()

class SituationProcessor:
    def __init__(self, nlp, rules, tags):
        self.nlp = nlp
        self.rules = rules
        self.tags = tags
        self.debug_flag = False
        self.response = ''

    def load_situation(self,situation):
        self.situation = str(situation.lower())

    def get_response(self):
        return self.response
    
    def get_predict(self):
        return self.predict

    def load_predict(self,predict):
        self.predict = predict
    
    def load_bert_settings(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model

    
    def debug_on(self):
        self.debug_flag = True

    def get_rules(self):
        self.debug(f"Analizando: {self.situation}")
        situation_doc = self.nlp(self.situation)
        situation_clean = self.preprocess(self.situation)
        matcher = self.match_filter_prepare(situation_doc)
        rules_result = []
        tags_rules_result = []
        similarity_sum = 0
        bert_similarity_sum = 0
        count_bert = 0
        flag_similar = False
        tags_similarity_sum = 0
        for rule in self.rules:
            self.debug(f"REGLA => {rule['nombre']}")
            # self.debug(f"CONTENIDO => {rule['contenido']}")
            rule_content_doc = self.nlp(rule["contenido"])
            rule_content_clean = self.preprocess(rule["contenido"])
            self.debug(f"Analizando: SIMILAR")
            similarity_info = self.similarity_filter(rule_content_doc,situation_doc)
            similarity_sum += similarity_info[1] if similarity_info[1] >= 0 else 0
            self.debug(f"Analizando: FILTER")
            match_info = self.match_filter(matcher, rule_content_doc)
            bert_similarity_info = False
            if (similarity_info[0] or match_info[0]):
                self.debug(f"Analizando: BERT SIMILAR1")
                count_bert += 1
                bert_similarity_info = self.bert_similarity(situation_clean,rule_content_clean)
                bert_similarity_sum += bert_similarity_info[1] if bert_similarity_info[1] >= 0 else 0
                if (bert_similarity_info[0]):
                    self.debug(f"AGREGA -----------------------------------")
                    rule["similarity"] = bert_similarity_info[1]
                    rule["match"] = match_info[1]
                    rules_result.append(rule)
                    continue
            if self.predict in rule['etiquetas']:
                self.debug(f"Analizando: BERT SIMILAR2")
                if (not bert_similarity_info):
                    count_bert += 1
                    bert_similarity_info = self.bert_similarity(situation_clean,rule_content_clean)
                    bert_similarity_sum += bert_similarity_info[1] if bert_similarity_info[1] >= 0 else 0
                    if (bert_similarity_info[0]):
                        rule["similarity"] = bert_similarity_info[1]
                        rules_result.append(rule)
                        continue
                tags_rules_result.append(rule)
        similarity_average = similarity_sum/len(self.rules)
        bert_similarity_average = bert_similarity_sum/count_bert
        self.debug(f"Promedio Similaridad: {similarity_average}")
        self.debug(f"Promedio Similaridad BERT: {bert_similarity_average}")
        print(f'UNO {bert_similarity_average} > 0.25 DOS {len(rules_result)} == {0}')
        if (bert_similarity_average > 0.35 and len(rules_result) == 0):
            print('ENTRA')
            #if (bert_similarity_average+similarity_average)/2 > 0.4:
            #print('ENTRA2')
            rules_result.extend(tags_rules_result)
        self.generate_response(rules_result)
        return rules_result
    
    def similarity_filter(self, rule_doc, situation_doc):
        similarity = situation_doc.similarity(rule_doc)
        if similarity > 0.7:
            self.debug(f'Similar {similarity}')
            return (True, similarity)
        else:
            self.debug(f'No similar {similarity}')
        return (False, similarity)
    
    def get_keywords(self, situation_doc, quantity=10):    
        keywords = [token.text.lower() for token in situation_doc if not token.is_stop and not token.is_punct]
        self.debug(f"KEYWORDS => {keywords}")
        count_keywords = Counter(keywords)
        common_keywords = count_keywords.most_common(quantity)
        return [word for word, _ in common_keywords]
    
    def match_filter_prepare(self, situation_doc):
        matcher = PhraseMatcher(self.nlp.vocab)
        keywords = self.get_keywords(situation_doc)
        for keyword in keywords:
            matcher.add(keyword, None, self.nlp(keyword))
        return matcher
    
    def match_filter(self, matcher, rule_doc):
        matches = matcher(rule_doc)
        ids = list(set([item[0] for item in matches]))
        self.debug(f"matches {len(ids)} / {len(matcher)} => {matches}")
        if (len(ids) and ( len(ids)/ len(matcher) > 0.7)):
            self.debug("MATCH")
            return (True,f"matches {len(ids)} / {len(matcher)} => {matches}")
        return (False,'')
    
    def clean_text(self, text, tags_flag=False):
        cleaned_text = ''
        if (tags_flag):
            cleaned_text = text.replace('<list>', '').replace('<list2>', '')
        cleaned_text = cleaned_text.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        cleaned_text = re.sub(r'[^a-zA-Z0-9áéíóúüÁÉÍÓÚÜ.,: ]', '', cleaned_text)
        return cleaned_text
    
    def preprocess(self, text):
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\d+', '', text)
        doc = self.nlp(text)
        words = [token.lemma_ for token in doc if token.text not in STOP_WORDS]
        return ' '.join(words)
    
    def get_bert_embeddings(self,text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)

    def bert_similarity(self, situation, content):
        text1_emb = self.get_bert_embeddings(situation)
        text2_emb = self.get_bert_embeddings(content)
        bert_similarity = torch.nn.functional.cosine_similarity(text1_emb, text2_emb).item()
        self.debug(f'SIMILARIDAD BERT: {bert_similarity}')
        return (bert_similarity > 0.7, bert_similarity)

    def generate_response(self, rules):
        if len(rules) == 0:
            self.response = "No encontramos ninguna norma relacionada con tu pregunta o situación."
            self.predict = None
            return 

        for tag in self.tags:
            if tag['nombre'] == self.predict:
                self.response = tag['respuesta']
                return
        
    def debug(self,message):
        if (self.debug_flag):
            print(message)
