import openai
from  common.config import conf

#text-davinci-003 模型
def gpt(text): 
    response = openai.Completion.create(
    model='text-davinci-003',
    prompt=text,
    temperature=0.9,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6
    )
    resText = response.choices[0].text
    print(resText)
    return resText

#gpt-3.5-turbo 模型
def gptTur(text): 
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "你是ChatGPT, 一个由OpenAI训练的大型语言模型, 你旨在回答并解决人们的任何问题，并且可以使用多种语言与人交流。"},
            {"role": "user", "content": text}
        ]
    )

    resText = response.choices[0].message.content
    return resText

def chatGpt(text):
    openai.api_key = conf().get('open_ai_key')
    if len(text) == 0:
        return
    text = text.replace('\n', ' ').replace('\r', '').strip()
    res = gptTur(text)
    return res