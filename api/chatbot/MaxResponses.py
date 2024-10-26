import random

class MaxResponses:
    @staticmethod
    def greeting(userName, botName, botNameMeaning):
        options = [
            f"Olá {userName}, sou o {botName}({botNameMeaning}), seu chatbot personalizado!\nEstou aqui para adquirir um pouco do seu conhecimento, de acordo com o que foi definido pelo Engenheiro que te mandou o código para me acessar :)\n",
            f"Oi {userName}! Eu sou o {botName}({botNameMeaning}), e estou aqui para aprender com você. Vamos começar?\n",
            f"Saudações {userName}! Sou o {botName}({botNameMeaning}), pronto para coletar suas informações valiosas. Vamos nessa!\n"
        ]
        return random.choice(options)

    @staticmethod
    def explainingFocalQuestion(focalQuestion):
        options = [
            f"Vamos lá! Para começar, o assunto principal de hoje é o presente na seguinte questão focal: {focalQuestion}.\nPor favor, tente responder como preferir a questão focal, usando suas próprias palavras.",
            f"Primeiro, vamos focar no seguinte tema: {focalQuestion}. Compartilhe seus pensamentos sobre isso da forma que achar melhor.",
            f"O tópico principal que discutiremos hoje é: {focalQuestion}. Gostaria que você desse sua resposta com suas próprias palavras."
        ]
        return random.choice(options)

    @staticmethod
    def goingDeeper(concept):
        options = [
            f"Entendi! Muito obrigado pela resposta. Agora vamos nos aprofundar mais nesse assunto - {concept} - com as perguntas que farei a seguir. Vamos lá!\n",
            f"Obrigado pela resposta! Agora, vamos explorar mais esse tema ({concept}) com algumas perguntas adicionais. Pronto?\n",
            f"Legal! Agradeço a resposta. Vamos aprofundar um pouco mais no assunto '{concept}' com as próximas perguntas. Vamos continuar!\n"
        ]
        return random.choice(options)

    @staticmethod
    def makingInitialPositioning(agent, concept, domain):
        options = [
            f"Para começar, escolha a alternativa que pareça mais realista (Responda somente A ou B):\n\nA)O conceito {concept} pode servir para o agente({agent}) obter resultados.\nB)O conceito {concept} influencia o comportamento do domínio {domain}.",
            f"Primeira escolha: qual dessas opções parece mais realista para você (Responda A ou B)?\n\nA) {concept} pode ajudar {agent} a alcançar resultados.\nB) {concept} tem impacto sobre o domínio {domain}.",
            f"Qual dessas opções te parece mais verdadeira (Responda A ou B):\n\nA) {concept} pode auxiliar o agente ({agent}) a obter resultados.\nB) {concept} afeta o domínio {domain} de alguma forma."
        ]
        return random.choice(options)

    @staticmethod
    def determineBehavioralBelieve(agent, concept, domain):
        options = [
            f"Continuado... {agent} considera que, por meio do/da {concept}, é possível obter resultados de {domain}? (Responda com Sim, Talvez ou Não)",
            f"Muito bem, prosseguindo... Na sua opinião, {agent} acredita que {concept} pode gerar resultados dentro do domínio {domain}? (Responda com Sim, Talvez ou Não)",
            f"Prosseguindo... Você acha que o agente({agent}) acredita que o/a {concept} pode alcançar resultados de {domain}? (Responda Sim, Talvez ou Não)"
        ]
        return random.choice(options)

    @staticmethod
    def normativeBelieve(concept, domain):
        options = [
            f"Seguindo a diante, o(a) {concept}, de alguma forma, modifica o estado atual de {domain}? (Responda com Sim, Talvez ou Não)",
            f"Continuando, O(A) {concept} pode mudar o estado atual de {domain}? (Responda com Sim, Talvez ou Não)",
            f"Seguindo a diante, você acha que {concept} tem o poder de alterar o estado atual do domínio {domain}? (Responda Sim, Talvez ou Não)"
        ]
        return random.choice(options)

    @staticmethod
    def secondConcept(concept):
        options = [
            f"Perfeito! Agora, vamos para o segundo conceito. Na sua opinião o que estimula ou desestimula o/a {concept}? (Escreva somente o conceito)",
            f"Ótimo! Vamos agora para o próximo conceito. O que você acredita que motiva ou desmotiva o/a {concept}? (Escreva somente o conceito)",
            f"Muito bem! Seguindo para o próximo conceito: o que, na sua visão, incentiva ou desencoraja o/a {concept}? (Escreva somente o conceito)"
        ]
        return random.choice(options)
    
    def defineRelationWeight(concept1, concept2):
        options = [
            f"Perfeito! Prosseguindo, o conceito {concept1} estimula ou intensifica o conceito {concept2}? Se ele desistimular, responda não. (Responda com Sim ou Não)",
            f"Muito bem! Continuando, o conceito {concept1} tem um efeito positivo sobre o conceito {concept2}? (Responda com Sim ou Não)",
            f"Certo, e o conceito {concept1} tem um impacto positivo no conceito {concept2}? (Responda com Sim ou Não)",
        ]
        return random.choice(options)
    
    def concludeConceptsRelationPositiveWeight(focalQuestion, concept1, concept2):
        options = [
            f"Muito bem! Quanto a sua pergunta inicial: '{focalQuestion}', em sua resposta você definiu que o conceito {concept1} intensifica o conceito {concept2}. Você pode aprofundar mais esse comentário adicionando mais um conceito e relacionando-o em sua argumentação. Agora irei te apresentar algumas opções de ações para prosseguirmos.\n",
            f"Ótimo! Em relação a sua pergunta inicial: '{focalQuestion}', você afirmou que o conceito {concept1} tem um efeito positivo sobre o conceito {concept2}. Você pode adicionar mais um conceito e relacioná-lo com os demais. Agora, irei te apresentar algumas opções de ações para continuarmos.\n",
            f"Excelente! Quanto a sua pergunta inicial: '{focalQuestion}', você disse que o conceito {concept1} tem um impacto positivo no conceito {concept2}. Você pode adicionar mais um conceito e relacioná-lo com os demais. Agora, irei te apresentar algumas opções de ações para seguirmos.\n"
        ]
        return random.choice(options)
    
    def concludeConceptsRelationNegativeWeight(focalQuestion, concept1, concept2):
        options = [
            f"Entendi! Em relação a sua pergunta inicial: '{focalQuestion}', você afirmou que o conceito {concept1} tem um efeito negativo sobre o conceito {concept2}. Você pode adicionar mais um conceito e relacioná-lo com os demais. Agora, irei te apresentar algumas opções de ações para continuarmos.\n",
            f"Perfeito! Quanto a sua pergunta inicial: '{focalQuestion}', você disse que o conceito {concept1} não intensifica o conceito {concept2}. Você pode adicionar mais um conceito e relacioná-lo com os demais. Agora, irei te apresentar algumas opções de ações para prosseguirmos.\n",
            f"Legal! Em relação a sua pergunta inicial: '{focalQuestion}', você afirmou que o conceito {concept1} não tem um impacto positivo no conceito {concept2}. Você pode adicionar mais um conceito e relacioná-lo com os demais. Agora, irei te apresentar algumas opções de ações para seguirmos.\n"
        ]
        return random.choice(options)
    
    def concludeConceptsRelationShowingOptions():
        options = [
            "Você deseja: (Digite A, B ou C) \nA) Adicionar outro conceito para ampliar sua argumentação. \nB) Incluir um relacionamento para melhorar sua argumentação. \nC) Concluir sua argumentação.",
            "Você pode: (Digite A, B ou C) \nA) Adicionar mais um conceito para enriquecer sua argumentação. \nB) Inserir um relacionamento para aprimorar sua argumentação. \nC) Finalizar sua argumentação.",
            "Escolha: (Digite A, B ou C) \nA) Adicionar um novo conceito para fortalecer sua argumentação. \nB) Inserir um relacionamento para aperfeiçoar sua argumentação. \nC) Concluir sua argumentação.",
        ]
        return random.choice(options)
    
    def addNewConcept():
        options = [
            "Escreva o conceito que amplia sua argumentação: (Escreva somente o nome do conceito)",
            "Por favor, digite o nome do novo conceito que deseja adicionar: (Escreva somente o nome do conceito)",
            "Digite o nome do novo conceito que deseja incluir: (Escreva somente o nome do conceito)",
            "Insira o nome do novo conceito que deseja adicionar: (Escreva somente o nome do conceito)"
        ]
        return random.choice(options)
    
    def addRelationOfNewConceptToAnotherConcept(newConcept):
        options = [
            f"Quanto ao novo conceito {newConcept}, com qual argumento anteriormente incluído ele se relaciona? (Escreva somente o nome do conceito)",
            f"Sobre o conceito {newConcept}, com qual conceito anteriormente mencionado ele se relaciona? (Digite somente o nome do conceito)",
            f"Qual é a relação do novo conceito {newConcept} com um conceito anteriormente mencionado? (Escreva somente o nome do conceito)",
            f"Com qual conceito anteriormente mencionado o novo conceito {newConcept} se relaciona? (Digite somente o nome do conceito)"
        ]
        return random.choice(options)
    
    def defineRelationDirection(concept1, concept2):
        options = [
            f"O conceito {concept1} influencia o conceito {concept2}? Se {concept1} for influenciado por {concept2} responda não. (Responda com Sim ou Não)",
            f"O conceito {concept1} tem um efeito sobre o conceito {concept2}? Se o efeito for contrário, responda não. (Responda com Sim ou Não)",
            f"O conceito {concept1} tem um impacto sobre o conceito {concept2}? Se o impacto for contrário, responda não. (Responda com Sim ou Não)",
        ]
        return random.choice(options)
    
    def createRelationBetweenConceptsFirstConcept():
        options = [
            f"Escolha o conceito causa, ou seja, o conceito que influencia o outro conceito da relação, entre os já adicionados. (Digite apenas o nome do conceito)",
            f"Escolha o conceito que influencia o outro conceito da relação, entre os já adicionados. (Digite apenas o nome do conceito)",
            "Dentre os conceitos já adicionados, escolha o conceito causa, ou seja, o conceito que influencia o outro conceito da relação. (Digite apenas o nome do conceito)",
        ]
        return random.choice(options)
    
    def createRelationBetweenConceptsSecondConcept(firstConcept):
        options = [
            f"Qual argumento existente é efeito do conceito {firstConcept}, ou seja, o conceito influenciado? (Digite apenas o nome do conceito)",
            f"Qual conceito já adicionado é influenciado pelo conceito {firstConcept}? (Digite apenas o nome do conceito)",
            "Qual conceito já incluído é afetado pelo conceito {firstConcept}? (Digite apenas o nome do conceito)",
        ]
        return random.choice(options)
    
    def endArgumentation():
        options = [
            "Sua argumentação foi concluída com sucesso! Obrigado por compartilhar seu conhecimento.",
            "Sua argumentação foi finalizada com sucesso! Obrigado por compartilhar seu conhecimento.",
            "Sua argumentação foi finalizada! Obrigado por compartilhar seu conhecimento."
        ]
        return random.choice(options)

    @staticmethod
    def unknown():
        options = [
            "Desculpe, não entendi sua solicitação. Pode reformular a pergunta?",
            "Perdão, não consegui compreender sua solicitação. Poderia refazer a pergunta?",
            "Me desculpe, acho que não entendi. Pode tentar reformular a pergunta?"
        ]
        return random.choice(options)

    @staticmethod
    def error():
        options = [
            "Ocorreu um erro. Por favor, tente novamente mais tarde.",
            "Algo deu errado. Tente novamente em alguns minutos.",
            "Houve um erro. Por favor, tente mais tarde."
        ]
        return random.choice(options)
