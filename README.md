 # GPIC: General Purpose Image Cruncher.

## Introduction
Chatgpt is very good at understanding images and this feature can be exploited to perform guidance in complex situations. 

####  Features
- Real time, scene by scene
- respond to visual changes (e.g. new 1m candle)
- prompts highly customizable
- Can select window or primary monitor
- Easy to use


#### Use cases
- Live visual tasks that require guidance
- Upstream module for creating text input in required format e.g. JSON for downstream tasks/controller.
- Livestream/Live video transcription (may not work for online video streaming websties)
- Real time Stock analysis
- Game assistant
- Homework helper

## Examples

### terminal prompt selection and window selection
![terminal](./examples/prompt_selection.png)

### Trading - Candlestick chart analysis

For example, in trading, traders often interpret candlestick charts visually. Traders use a method called technical analysis which is complicated (involves many complicated patterns and measures) and highly subjective, and can lead to losses if inaccurate. Many traders, and especially beginners also have very little knowledge of technical analysis. One way is to rely (at your own peril) on chatgpt to analyse the candlestick graphs and provide trading advice. In this case, the LLM assistant can be deployed in which it will analyse the stock chart when it detects a change and output its analysis in text form and provide guidance to the trader. 

Beyond trading, this is a general purpose method and can be used for other scenarios that require LLM assistance.


![stock](./examples/stock.png)
![response](./examples/stock-result.png)


### Game assistant

![dota2](./examples/dota2.png)
![response](./examples/dota2-result.png)


Set up:
```bash
conda create -n assistant python=3.12
pip install -r requirements.txt
```

Setup openai api key:
```bash
export OPENAI_API_KEY="sk-your_api_key_here"
```

Run:
```bash
cd main
python chatgpt_assistant.py
```
