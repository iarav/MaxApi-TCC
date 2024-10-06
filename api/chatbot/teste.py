from transformers import GPT2LMHeadModel, GPT2Tokenizer
from MaxResponses import MaxResponses

model_name = "pierreguillou/gpt2-small-portuguese"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
model.config.pad_token_id = model.config.eos_token_id

def paraphrase_pt(sentence):
    inputs = tokenizer.encode(sentence, return_tensors='pt')
    attention_mask = inputs.ne(tokenizer.pad_token_id).long()
    
    outputs = model.generate(
        inputs,
        attention_mask=attention_mask,  
        max_length=300,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        pad_token_id=tokenizer.eos_token_id 
    )
    return [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    
responseTest = "Leia a seguinte frase e a partir dela, mude as palavras mantendo o significado e sem adicionar novas coisas, apenas trocando as palavrar da frase por sinonimos. A frase é a seguinte: " + MaxResponses.greeting("Iara", "MAX", "Management and Acquisition eXpert")
responseTest2 = MaxResponses.explainingFocalQuestion("O que você acha sobre a inteligência artificial no ambiente escolar?")
responseTest3 = MaxResponses.goingDeeper("conceito X")
responseTest4 = MaxResponses.makingInitialPositioning("você", "inteligência artificial", "ambiente escolar")
sentences = [responseTest, responseTest2, responseTest3, responseTest4]

print("\n\n\n-----------------------------------------------------------------------------------------------")
for sentence in sentences:
    print("Original sentence: ")
    print(sentence)
    parafrases = paraphrase_pt(sentence)
    print("Paraphrases: ")
    print(parafrases)     
    print("-----------------------------------------------------------------------------------------------\n\n")   
    