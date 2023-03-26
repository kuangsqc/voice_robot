# 简介

基于ChatGPT的语言聊天机器人，通过picovoice语言唤醒对话，采用google语音识别引擎解析语言内容，再通过ChatGPT接口生成对话内容和微软未公开接口合成语言。

# 快速开始

## 准备

### 1. OpenAI账号注册

前往 [OpenAI注册页面](https://beta.openai.com/signup) 创建账号，参考这篇 [教程](https://www.pythonthree.com/register-openai-chatgpt/) 可以通过虚拟手机号来接收验证码。创建完账号则前往 [API管理页面](https://beta.openai.com/account/api-keys) 创建一个 API Key 并保存下来，后面需要在项目中配置这个key。

### 2.Picovoice账号注册

前往[Picovoice注册页面](https://console.picovoice.ai/) 创建账号，生成AccessKey并保存下来，后面需要在项目中配置这个AccessKey。如果需要训练自己的唤醒词在这个页面[唤醒词训练页面](https://console.picovoice.ai/ppn)，选择“English”，输入唤醒次训练导出。本项目默认唤醒词“hey Tony”，可直接使用。

### 3.运行环境

 
Python版本在 3.7.1以上。按requirement.txt安装依赖库。


## 配置

配置文件的模板在根目录的`config.template.json`中，需复制该模板创建最终生效的 `config.json` 文件：

```bash
  cp config.template.json config.json
```

然后在`config.json`中填入配置，以下是对默认配置的说明，可根据需要进行自定义修改：

```bash
# config.json文件内容示例
{ 
  "open_ai_key": "YOUR API KEY",                         # 填入OpenAI创建的 OpenAI API KEY
  "picovoice_access_key": "",                            # 填入picovoice创建的 AccessKey
  "picovoice_ppn": ".\\model\\hey-tony.ppn",             # 唤醒词模型路径
  "proxy": "http://127.0.0.1:7890",                      # 代理客户端的ip和端口
}
```

## 运行

```bash
  python main.py
```

试着说“hey Tony”对话。
