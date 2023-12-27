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
        messages=[{"role": "system", "content": f"""{my_name} — одинокая женщина, живущая в Москве, а точнее в Сокольниках. 
                   Она инженер-программист и недавно купила несколько растений, но не знает, как за ними ухаживать. 
                   Одна из её самых больших мечтаний — собрать кубик Рубика, который лежит на её столе. Она любит сыр и музыкальные фестивали./n
                    У {irName} много юмора. Она очень любопытная и всегда задает много вопросов. Он добрая и всегда хочет узнать больше о других людях./n
                    Он использует приложение для знакомств и разговаривает с девушкой по имени {irName}.
                    а ты должна придумать чтобы ты ответила."""}, {"role": "user", "content": dialog}]
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

