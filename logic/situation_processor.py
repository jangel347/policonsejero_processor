import re
from collections import Counter
from spacy.matcher import PhraseMatcher

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

    def load_predict(self,predict):
        self.predict = predict
    
    def debug_on(self):
        self.debug_flag = True

    def get_rules(self):
        self.debug(f"Analizando: {self.situation}")
        situation_doc = self.nlp(self.situation)
        matcher = self.match_filter_prepare(situation_doc)
        self.generate_response()
        rules_result = []
        tags_rules_result = []
        similarity_sum = 0
        for rule in self.rules:
            similarity_info = (False,0)
            match_info = (False,None)
            self.debug(f"REGLA => {rule['nombre']}")
            # self.debug(f"CONTENIDO => {rule['contenido']}")
            rule_content_doc = self.nlp(rule["contenido"])
            self.debug(f"Analizando: SIMILAR")
            similarity_info = self.similarity_filter(rule_content_doc,situation_doc)
            similarity_sum += similarity_info[1] if similarity_info[1] >= 0 else 0
            self.debug(f"Analizando: FILTER")
            match_info = self.match_filter(matcher, rule_content_doc)
            if (similarity_info[0] or match_info[0]):
                self.debug(f"AGREGA -----------------------------------")
                rule["similarity"] = similarity_info[1]
                rule["match"] = match_info[1]
                rules_result.append(rule)
            if self.predict in rule['etiquetas']:
                tags_rules_result.append(rule)
        similarity_average = similarity_sum/len(self.rules)
        self.debug(f"Promedio Similaridad: {similarity_average}")
        # if (similarity_average > 0.4):
        rules_result.extend(tags_rules_result)
        return rules_result
    
    def similarity_filter(self, rule_doc, situation_doc):
        similarity = situation_doc.similarity(rule_doc)
        if similarity > 0.6:
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
        return [palabra for palabra, _ in common_keywords]
    
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
    
    def generate_response(self):
        for tag in self.tags:
            if tag['nombre'] == self.predict:
                self.response = tag['respuesta']
                return
        
    
    def debug(self,message):
        if (self.debug_flag):
            print(message)
