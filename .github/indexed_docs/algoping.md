> This resource is auto indexed by AwesomeAlgo, all credits to algoping, for more details refer to https://github.com/aorumbayev/algoping

---

<br/>
<div align="center">
<a href="https://github.com/aorumbayev/awesome-algorand"><img src="https://bafkreihb4jprrzqdswxohr3wrlxh74hjmo4vglbotf6ozp4xh2lma7var4.ipfs.nftstorage.link"></a>
</div>
<br/>
<div align="center">
📣 I am a free and open source health monitoring bot for Algorand Developers that issues a <a href="https://twitter.com/algoping">tweet</a> with statistics on number of block proposals and other useful daily information.
<br />
<br />
</div>

<p align="center">
    <img  src="https://visitor-badge.glitch.me/badge?page_id=aorumbayev.algoping&right_color=green" />
    <a target="_blank" href="https://twitter.com/algoping">
        <img src="https://img.shields.io/badge/Browse-Twitter-green.svg" />
    </a>
    <a target="_blank" href="https://algoping.betteruptime.com">
        <img src="https://img.shields.io/badge/Browse-StatusPage-green.svg" />
    </a>
    <a href="https://github.com/aorumbayev/algoping">
        <img src="https://img.shields.io/github/stars/aorumbayev/algoping?color=green" />
    </a>
    <a  href="https://github.com/aorumbayev/algoping/network/members">
        <img src="https://img.shields.io/github/forks/aorumbayev/algoping?color=green" />
    </a>
</p>

## About

### What is AlgoPing?

**1. Analytics Tweet Bot**:

AlgoPing is a daily cron triggered bot that uses [BitQuery](https://bitquery.io/) GraphQL API to fetch daily stats on total amount of block proposals and info on proposers. It then uses [Tweepy](https://www.tweepy.org/) to post a tweet with the stats on daily basis to [@algoping](https://twitter.com/algoping) Twitter account.

**2. Health Monitoring Status Page**:

Additionally, AlgoPing uses [BetterUptime](https://betteruptime.com/) to monitor the status of Node and Indexer servers provided by [AlgoNode](https://algonode.io/) and [AlgoExplorer](https://algoexplorer.io/) respectively. Please note the status page is not affiliated with AlgoNode or AlgoExplorer, for official status refer to their respective websites and communication channels. The aim is to simply provide a free unnoficial status page for the Algorand community that aggregates different Node and Indexer Providers.

> Please note there are not source codes for health monitoring as AlgoPing relies on a free tier on a third party provider named [BetterUptime](https://betteruptime.com/). If you are interested in setting up your own health monitoring status page, please refer to [BetterUptime](https://betteruptime.com/) documentation.

## Prerequisites

-   [python 3.9.x](https://www.python.org/)
-   [poetry](https://python-poetry.org/)
-   [pre-commit](https://pre-commit.com/)

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

-   `BITQUERY_API_KEY` - Specify Bitquery GraphQL API key to get daily stats on total amount of block proposals and info on proposers.

Once you have your credentials, you can run the bot locally with:

```bash
PYTHONPATH="." poetry run python src/analytics.py
```

## Contributing

Contributions are welcome if you want to improve existing setup of the bot that is currently reporting to [AlgoPing](https://twitter.com/algoping) twitter account.

Otherwise, feel free to clone it and tweak it for your needs to run the bot on your own twitter account.
