import spacy

nlp = spacy.load('pt_core_news_sm')

def extractEntitiesFocalQuestion(focalQuestion):
    doc = nlp(focalQuestion)
    entities = {}
    possibleWords = [
        'contexto', 'dominio', 'domínio', 'cenário', 'cenario',
        'área', 'area', 'assunto', 'tema', 'contextualização',
        'contextualizacao', 'ambiente', 'âmbito', 'campo', 'esfera',
        'universo', 'território', 'territorialidade', 'abrangência', 'relação'
    ]

    notAgentWords = [
        'perspectiva', 'opinião', 'visão', 'entendimento', 'concepção'
    ]
    
    agent, domain, concept = None, None, None

    ignored_words = ['da', 'na', 'em', 'de', 'do', 'à', 'as', 'e', 'que', 'ou', 'no', 'os', 'um', 'uma', 'para', 'sobre', 'com', 'sua', 'seu', 'relevância', 'relevancia', 'dos', 'das', 'são', 'é', 'o', 'a', 'os', 'as', 'sobre', 'de', 'em', 'na', 'no', 'do', 'da', 'à', 'às', 'aos', 'e', 'ou', 'com', 'como', 'qual', 'quais', 'quando', 'quando', 'quem', 'quanto', 'quanta', 'quantos', 'quantas', 'por', 'para', 'porque', 'porquê', 'porquanto', 'porquanto']

    for i, token in enumerate(doc):
        if 'subj' in token.dep_ and token.text not in notAgentWords:
            agent = token.text
            
        elif token.dep_ in ['obj', 'nmod', 'obl'] and token.text not in ignored_words:
            if token.head.lemma_ in possibleWords or token.head.head.lemma_ in possibleWords:
                if domain is None:
                    domain = token.text
                    if doc[i - 1].text not in ignored_words and doc[i - 1].dep_ in ['obj', 'nmod', 'obl', 'compound', 'amod']:
                        domain = doc[i - 1].text + " " + concept
                    if doc[i + 1].text not in ignored_words and doc[i + 1].dep_ in ['obj', 'nmod', 'obl', 'compound', 'amod']:
                        domain += " " + doc[i + 1].text
            
            elif token.text not in possibleWords:
                if concept is None:
                    concept = token.text
                    if doc[i - 1].text not in ignored_words and doc[i - 1].dep_ in ['obj', 'nmod', 'obl', 'compound', 'amod']:
                        concept = doc[i - 1].text + " " + concept
                    if doc[i + 1].text not in ignored_words and doc[i + 1].dep_ in ['obj', 'nmod', 'obl', 'compound', 'amod']:
                        concept += " " + doc[i + 1].text

    entities['AGENT'] = agent if agent else None
    entities['CONCEPT'] = concept if concept else None
    entities['DOMAIN'] = domain if domain else None

    return entities