import spacy
from typing import Dict, Tuple, List, Optional

class EntityExtractor:
    def __init__(self, model: str = 'pt_core_news_sm'):
        self.nlp = spacy.load(model)
        self.possibleWords = self._getPossibleWords()
        self.notAgentWords = ['perspectiva', 'opinião', 'visão', 'entendimento', 'concepção', 'percepção', 'ponto de vista', 'relevância', 'importância']
        self.ignoredWords = self._getIgnoredWords()

    @staticmethod
    def _getPossibleWords() -> List[str]:
        return [
            'abrangência', 'ambiente', 'área', 'area', 'assunto', 'campo', 
            'cenário', 'cenario', 'contexto', 'contextualização', 
            'contextualizacao', 'dominio', 'domínio', 'esfera', 'relação', 
            'tema', 'territorialidade', 'território', 'universo', 'âmbito'
        ]

    @staticmethod
    def _getIgnoredWords() -> List[str]:
        return [
            'aos', 'as', 'com', 'como', 'da', 'das', 'de', 'do', 'dos', 'e', 
            'em', 'importância', 'influência', 'na', 'nas', 'no', 'nos', 'o', 
            'os', 'ou', 'para', 'pela', 'pelos', 'pelo', 'por', 'porque', 
            'porquanto', 'porquê', 'qual', 'quais', 'quando', 'quanto', 
            'quanta', 'quantas', 'quantos', 'que', 'quem', 'relevancia', 
            'relevância', 'são', 'seu', 'sobre', 'sua', 'um', 'uma', 'à', 
            'às', 'é'
        ]

    def extractEntities(self, focalQuestion: str) -> Dict[str, Optional[str]]:
        doc = self.nlp(focalQuestion)
        agent, domain, concept = self._extractAgentDomainConcept(doc)

        # If domain is still None, try to extract from the end of the sentence
        if domain is None:
            domain = self._extractDomainFromEnd(doc)
        
        return {
            'AGENT': agent,
            'CONCEPT': concept,
            'DOMAIN': domain
        }

    def _extractAgentDomainConcept(self, doc) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        agent, domain, concept = None, None, None

        for i, token in enumerate(doc):
            if 'subj' in token.dep_ and token.text not in self.notAgentWords:
                agent = token.text
            
            elif token.dep_ in ['obj', 'nmod', 'obl'] and token.text not in self.ignoredWords:
                if self._isDomainWord(token) and domain is None:
                    domain = self._getCombinedEntity(token, doc, i, domain)
                elif token.text not in self.possibleWords and concept is None:
                    concept = self._getCombinedEntity(token, doc, i, concept)

        return agent, domain, concept

    def _isDomainWord(self, token) -> bool:
        return token.head.lemma_ in self.possibleWords or token.head.head.lemma_ in self.possibleWords

    def _getCombinedEntity(self, token, doc, index: int, currentEntity: Optional[str]) -> str:
        entity = token.text

        if currentEntity:
            entity = currentEntity + " " + entity
        
        while index > 0 and self._validateCombinedEntity(doc[index - 1]):
            entity = doc[index - 1].text + " " + entity
            index -= 1

        while index < len(doc) - 1 and self._validateCombinedEntity(doc[index + 1]):
            entity += " " + doc[index + 1].text
            index += 1
        
        return entity
    
    def _validateCombinedEntity(self, token) -> bool:
        return token.text not in self.ignoredWords and token.dep_ in ['obj', 'nmod', 'obl', 'compound', 'amod', 'case']
    
    def _extractDomainFromEnd(self, doc) -> Optional[str]:
        last_words = []
        for token in reversed(doc):
            if token.text not in self.ignoredWords:
                last_words.append(token.text)
            else:
                break
        return " ".join(reversed(last_words)) if last_words else None
