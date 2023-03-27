<br/>
<div align="center">
<a href="https://github.com/aorumbayev/awesome-algorand"><img src="https://i.imgur.com/bffzQBG.png"></a>
</div>
<br/>
<div align="center">
📣 I am a free and open source health monitoring bot for Algorand Developers that issues a <a href="https://twitter.com/algoping">tweet</a> when <a href="http://AlgoExplorer.io">AlgoExplorer</a> or <a href="http://AlgoNode.io">AlgoNode</a>'s node or indexer health endpoints experience outages.
<br />
<br />
</div>

<p align="center">
    <img  src="https://visitor-badge.glitch.me/badge?page_id=aorumbayev.algoping&right_color=teal" />
    <a target="_blank" href="https://twitter.com/algoping">
        <img src="https://img.shields.io/badge/Browse-Twitter-teal.svg" />
    </a>
    <a href="https://github.com/aorumbayev/algoping">
        <img src="https://img.shields.io/github/stars/aorumbayev/algoping?color=teal" />
    </a>
    <a  href="https://github.com/aorumbayev/algoping/network/members">
        <img src="https://img.shields.io/github/forks/aorumbayev/algoping?color=teal" />
    </a>
</p>

## About

### What is AlgoPing?

AlgoPing is a free and open source health monitoring and block analytics bot for Algorand Developers that issues a [tweet](https://twitter.com/algoping) when [AlgoExplorer](http://AlgoExplorer.io) or [AlgoNode](http://AlgoNode.io)'s node or indexer health endpoints experience outages as well as daily statistics. If you want to add more public node providers to the list, please submit a pull request ❤️

### Why AlgoPing?

Relying on free GitHub infrastructure allows this bot to be executed every 30 minutes via GitHub Actions. This means that AlgoPing will be able to monitor AlgoExplorer and AlgoNode's health endpoints for outages 24/7. Any developer in Algorand ecosystem can simply subsribe to the twitter account and be notified when AlgoExplorer or AlgoNode's health endpoints experience outages in real time.

Additionally, AlgoPing relies on Bitquery GraphQL API to get daily stats on total amount of block proposals and info on proposers.

### How does AlgoPing work?

AlgoPing runs a multithreaded Python script that checks the health endpoints of AlgoExplorer and AlgoNode triggered every `60` minutes. Once executed it independently queries AlgoNode and AlgoExplorer endpoints for `DURATION_SECONDS` and counts ratio of unsuccessful requests. If the ratio in relation to total amount requests made within `DURATION_SECONDS` (with `LIVENESS_DELAY_SECONDS` delay in between rounds) is greater than 50%, this means that within the `DURATION_SECONDS` minutes triggered execution timeframe the endpoints were down for at least `DURATION_SECONDS / 2` seconds. Hence, AlgoPing will issue a tweet to the [AlgoPing Twitter account](https://twitter.com/algoping) that some endpoints where down in the past `DURATION_SECONDS` minutes timeframe.

If you want to contribute and improve the health monitoring logic of AlgoPing, please feel free to submit a pull request ❤️

## Prerequisites

- [python 3.9.x](https://www.python.org/)
- [poetry](https://python-poetry.org/)
- [pre-commit](https://pre-commit.com/)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/aorumbayev/algoping.git && cd algoping
```

2. Install dependencies:

```bash
poetry install
```

3. Install pre-commit hooks:

```bash
pre-commit install
```

4. Done 🎉

## Usage

Create twitter app and get your credentials. The following environment variables are required by [`tweepy`](https://www.tweepy.org/):

- `BEARER_TOKEN` - (required) - obtain from Twitter Developers portal. Refer to tweepy documentation.
- `CONSUMER_KEY` - (required) - obtain from Twitter Developers portal. Refer to tweepy documentation.
- `CONSUMER_SECRET` - (required) - obtain from Twitter Developers portal. Refer to tweepy documentation.
- `ACCESS_TOKEN` - (required) - obtain from Twitter Developers portal. Refer to tweepy documentation.
- `ACCESS_TOKEN_SECRET` - (required) - obtain from Twitter Developers portal. Refer to tweepy documentation.
- `DURATION_SECONDS` - (optional) specify total duration for executing health checks in seconds, defaults to 30 minutes.
- `LIVENESS_DELAY_SECONDS` - (optional) specify the delay in between liveness checks, defaults to 5 seconds.
- `BITQUERY_API_KEY` - (optional) specify Bitquery GraphQL API key to get daily stats on total amount of block proposals and info on proposers.

Once you have your credentials, you can run the bot locally with:

```bash
PYTHONPATH="." poetry run python src/algoping.py
```

If you want to run the analytics instead:

```bash
PYTHONPATH="." poetry run python src/analytics.py
```

## Contributing

Contributions are welcome if you want to improve existing setup of the bot that is currently reporting to [AlgoPing](https://twitter.com/algoping) twitter account.

Otherwise, feel free to clone it and tweak it for your needs to run the bot on your own twitter account.
