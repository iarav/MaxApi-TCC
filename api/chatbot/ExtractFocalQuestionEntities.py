import spacy
from typing import Dict, Tuple, List, Optional

class EntityExtractor:
    def __init__(self, model: str = 'pt_core_news_sm'):
        self.nlp = spacy.load(model)
        self.possibleWords = self._getPossibleWords()
        self.notAgentWords = ['perspectiva', 'opinião', 'visão', 'entendimento', 'concepção']
        self.ignoredWords = self._getIgnoredWords()

    @staticmethod
    def _getPossibleWords() -> List[str]:
        return [
            'contexto', 'dominio', 'domínio', 'cenário', 'cenario',
            'área', 'area', 'assunto', 'tema', 'contextualização',
            'contextualizacao', 'ambiente', 'âmbito', 'campo', 'esfera',
            'universo', 'território', 'territorialidade', 'abrangência', 'relação'
        ]

    @staticmethod
    def _getIgnoredWords() -> List[str]:
        return [
            'da', 'na', 'em', 'de', 'do', 'à', 'as', 'e', 'que', 'ou', 'no', 
            'os', 'um', 'uma', 'para', 'sobre', 'com', 'sua', 'seu', 'relevância', 
            'relevancia', 'dos', 'das', 'são', 'é', 'o', 'a', 'os', 'as', 'sobre', 
            'de', 'em', 'na', 'no', 'do', 'da', 'à', 'às', 'aos', 'e', 'ou', 
            'com', 'como', 'qual', 'quais', 'quando', 'quem', 'quanto', 
            'quanta', 'quantos', 'quantas', 'por', 'para', 'porque', 
            'porquê', 'porquanto'
        ]

    def extractEntities(self, focalQuestion: str) -> Dict[str, Optional[str]]:
        doc = self.nlp(focalQuestion)
        agent, domain, concept = self._extractAgentDomainConcept(doc)
        
        return {
            'AGENT': agent,
            'DOMAIN': domain,
            'CONCEPT': concept
        }

    def _extractAgentDomainConcept(self, doc) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        agent, domain, concept = None, None, None

        for i, token in enumerate(doc):
            if 'subj' in token.dep_ and token.text not in self.notAgentWords:
                agent = token.text
            
            elif token.dep_ in ['obj', 'nmod', 'obl'] and token.text not in self.ignoredWords:
                if self._isDomainWord(token):
                    domain = self._getCombinedEntity(token, doc, i, domain)
                elif token.text not in self.possibleWords:
                    concept = self._getCombinedEntity(token, doc, i, concept)

        return agent, domain, concept

    def _isDomainWord(self, token) -> bool:
        return token.head.lemma_ in self.possibleWords or token.head.head.lemma_ in self.possibleWords

    def _getCombinedEntity(self, token, doc, index: int, currentEntity: Optional[str]) -> str:
        entity = token.text

        if currentEntity:
            entity = currentEntity + " " + entity
        
        if index > 0 and doc[index - 1].text not in self.ignoredWords and doc[index - 1].dep_ in ['obj', 'nmod', 'obl', 'compound', 'amod']:
            entity = doc[index - 1].text + " " + entity
        
        if index < len(doc) - 1 and doc[index + 1].text not in self.ignoredWords and doc[index + 1].dep_ in ['obj', 'nmod', 'obl', 'compound', 'amod']:
            entity += " " + doc[index + 1].text
        
        return entity