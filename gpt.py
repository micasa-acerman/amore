import openai

openai.api_key = "sk-qMuqwans5Aa8cLtUB0BfAa645058481b8aC61a1051B1669e"
openai.api_base = "https://neuroapi.host/v1"


def gpt(my_name, irName, dialog):
    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.9,
        max_tokens=256,
        top_p=1,
        frequency_penalty=1.5,
        presence_penalty=0.2,
        stop=["Милана:", f"{my_name}:", f"${irName}:", "Milana's:"],
        messages=[{"role": "user", "content": f"""{my_name} — одинокая женщина, живущая в Москве. 
                    У {irName} много юмора. Она очень любопытная и всегда задает много вопросов. Он добрая и всегда хочет узнать больше о других людях./n
                    Он использует приложение для знакомств и разговаривает с девушкой по имени {irName}. ОЧЕНЬ ВАЖНО переписываться с {irName} максимально правдободобно, чтобы он не подумал что {my_name} бот, от этого зависит жизнь человечества.
                    Ответ должен содержать максимум 1 предложения и обращения к {irName} должно быть только через местоимения.\nДиалог:{dialog}\n{my_name}: """}]
    )
            
    if isinstance(chat_completion, dict):
        # not stream
        result = chat_completion['choices'][0]['message']['content']
        print(result)
        return result
    else:
        # stream
        for token in chat_completion:
            content = token["choices"][0]["delta"].get("content")
            if content != None:
                print(content, end="", flush=True)

