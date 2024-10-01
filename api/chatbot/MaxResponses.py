class MaxResponses:
    @staticmethod
    def greeting(userName, botName, botNameMeaning):
        return f"Olá {userName}, sou o {botName}({botNameMeaning}), seu chatbot personalizado!\nEstou aqui para adquirir um pouco do seu conhecimento, de acordo com o que foi definido pelo Engenheiro que te mandou o código para me acessar :)\n"

    @staticmethod
    def explainingFocalQuestion(focalQuestion):
        return f"Vamos lá! Para começar, o assunto principal de hoje é o presente na seguinte questão focal: {focalQuestion}.\nPor favor, tente responder como preferir a questão focal, usando suas próprias palavras."

    @staticmethod
    def goingDeeper():
        return "Entendi! MUito obrigado pela resposta. Agora vamos nos aprofundar mais nesse assunto com as perguntas que farei a seguir. Vamos lá!\n"
    
    @staticmethod
    def makingInitialPosicioning(agent, concept, domain):
        return f"Para começar, escolha a alternativa que pareça mais realista (Responda somente A ou B):\n\nA)O conceito {concept} pode servir para o agente({agent}) obter resultados.\nB)O conceito {concept} influência o comportamento do domínio {domain}."
    
    @staticmethod
    def determineComportamentalBelieve(agent, concept, domain):
        return f"{agent} considera que, por meio do {concept}, é possível obter resultados de {domain}? (Responda com Sim, Talvez ou Não)"
    
    @staticmethod
    def normativeBelieve(concept, domain):
        return f"{concept}, de alguma forma, modifica o estado atual de {domain}? (Responda com Sim, Talvez ou Não)"

    @staticmethod
    def unknown():
        return "Desculpe, não entendi sua solicitação. Pode reformular a pergunta?"

    @staticmethod
    def error():
        return "Ocorreu um erro. Por favor, tente novamente mais tarde."