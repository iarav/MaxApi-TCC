class MaxResponses:
    @staticmethod
    def greeting(userName):
        return f"Olá {userName}, sou o MAX, seu chatbot personalizado!\nEstou aqui para adquirir um pouco do seu conhecimento, de acordo com o que foi definido pelo Engenheiro que te mandou o código para me acessar :)"

    @staticmethod
    def farewell(name):
        return f"Adeus, {name}! Tenha um ótimo dia!"

    @staticmethod
    def help():
        return "Aqui estão algumas coisas que posso fazer por você: responder perguntas, fornecer informações e muito mais."

    @staticmethod
    def unknown():
        return "Desculpe, não entendi sua solicitação. Pode reformular a pergunta?"

    @staticmethod
    def info(topic):
        return f"Aqui está a informação que encontrei sobre {topic}."

    @staticmethod
    def error():
        return "Ocorreu um erro. Por favor, tente novamente mais tarde."

# Exemplo de uso:
# from MaxResponses import MaxResponses
# print(MaxResponses.greeting("João"))
# print(MaxResponses.info("Python"))