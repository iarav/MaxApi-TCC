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
            f"{agent} considera que, por meio do/da {concept}, é possível obter resultados de {domain}? (Responda com Sim, Talvez ou Não)",
            f"Na sua opinião, {agent} acredita que {concept} pode gerar resultados dentro do domínio {domain}? (Responda com Sim, Talvez ou Não)",
            f"Você acha que o agente({agent}) acredita que o/a {concept} pode alcançar resultados de {domain}? (Responda Sim, Talvez ou Não)"
        ]
        return random.choice(options)

    @staticmethod
    def normativeBelieve(concept, domain):
        options = [
            f"{concept}, de alguma forma, modifica o estado atual de {domain}? (Responda com Sim, Talvez ou Não)",
            f"O/A {concept} pode mudar o estado atual de {domain}? (Responda com Sim, Talvez ou Não)",
            f"Você acha que {concept} tem o poder de alterar o estado atual do domínio {domain}? (Responda Sim, Talvez ou Não)"
        ]
        return random.choice(options)

    @staticmethod
    def secondConcept(concept):
        options = [
            f"Agora, vamos para o segundo conceito. Na sua opinião o que estimula ou desestimula o/a {concept}?",
            f"Vamos agora para o próximo conceito. O que você acredita que motiva ou desmotiva o/a {concept}?",
            f"Seguindo para o próximo conceito: o que, na sua visão, incentiva ou desencoraja o/a {concept}?"
        ]
        return random.choice(options)
    
    def defineRelationWeight(concept1, concept2):
        options = [
            f"O conceito {concept1} estimula ou intensifica o conceito {concept2}? Se ele desistimular, responda não. (Responda com Sim ou Não)",
            f"O conceito {concept1} tem um efeito positivo sobre o conceito {concept2}? (Responda com Sim ou Não)",
            f"O conceito {concept1} tem um impacto positivo no conceito {concept2}? (Responda com Sim ou Não)",
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
