import spacy

# Load the language model for NLP
nlp = spacy.load('pt_core_news_sm')

def extractEntitiesFocalQuestion(focalQuestion):
    doc = nlp(focalQuestion)
    entities = {}

    possibleWords = ['contexto', 'dominio', 'domínio', 'cenário', 'cenario']

    # Finding entities
    for token in doc:
        # Searching for the subject
        if 'subj' in token.dep_:
            entities['AGENT'] = token.text
        # Searching for objects ou nominal complements
        elif token.dep_ in ['obj', 'nmod', 'obl']:
            if token.head.lemma_ in possibleWords or token.head.head.lemma_ in possibleWords:
                entities['DOMAIN'] = token.text
            elif not(token.text in possibleWords):
                entities['CONCEPT'] = token.text
        # else:
        #     print(token.text + "não é nunhum, é: " + str(token.dep_))

    return entities