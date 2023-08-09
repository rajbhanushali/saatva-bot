# Saatva Mattress Website Chatbot

This repository contains a Slack chatbot that is designed to scrape data from the saatva.com website, process it, and provide relevant responses to user queries using the power of natural language processing.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The main goal of this project is to build a Slack chatbot that can answer user queries related to Saatva mattresses. The chatbot employs a combination of web scraping, natural language processing, and machine learning techniques to understand user queries and provide appropriate responses. The core components of the chatbot are:

1. **scrape_data.ipynb**: A Jupyter notebook that uses Python to scrape data from the Saatva website. It collects product descriptions, reviews, and other relevant information.

2. **slack_bot.py**: The main script that powers the Slack chatbot. It listens for incoming messages from users, performs similarity searches against the Pinecone database, and returns relevant excerpts based on the user's query.

**llama-2-7b-chat**: A large language model hosted on a Hugging Face inference endpoint. This model helps generate detailed responses for the user based on the extracted information from the Saatva website.

## Getting Started

To get started with the Saatva Mattress Website Chatbot, follow these steps:

1. Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/your-username/saatva-mattress-chatbot.git
```

2. Install the required Python dependencies by running:

```bash
pip install -r requirements.txt
```

3. Set up a Slack app and obtain the necessary API keys and tokens for the chatbot to function. This will require creating a new bot user for your Slack workspace.

4. Create a Pinecone account and set up a Vector Database to store the embeddings generated from the scraped data.

5. Obtain access to the Hugging Face inference endpoint and get the necessary credentials for communication with the "llama-2-7b-chat" language model.

## Usage

1. Run the `scrape_data.ipynb` notebook to collect data from the Saatva website and generate sentence embeddings using the sentence transformer model.

2. Start the Slack bot by running the `slack_bot.py` script:

```bash
python slack_bot.py
```

3. Interact with the bot in your Slack workspace by sending messages. The bot will respond to your queries with relevant information from the Saatva website.

## Requirements

- Python 3.7 or higher
- Jupyter Notebook
- Python packages listed in `requirements.txt`
- Slack API keys and tokens
- Pinecone Vector Database
- Hugging Face inference endpoint credentials
