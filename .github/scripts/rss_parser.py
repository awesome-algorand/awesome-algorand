from typing import List
import feedparser
import markdownify
from dataclasses import dataclass
import json


@dataclass
class PodcastEpisode:
    title: str
    description: str
    summary: str
    link: str
    published: str
    cover_image: str
    audio_url: str
    id: str
    episode: str
    season: str


def save_podcast_episodes_to_json(episodes: List[PodcastEpisode], file_path: str):
    # Convert the list of PodcastEpisode objects to a list of dictionaries
    # that can be serialized to JSON
    episodes_data = [episode.__dict__ for episode in episodes]

    # Write the JSON data to the specified file
    with open(file_path, "w") as f:
        json.dump(episodes_data, f, indent=2)
        print(f"Saved {len(episodes_data)} episodes to {file_path}")


def parse_awesome_feed(feed_url: str):
    NewsFeed = feedparser.parse(feed_url)

    episodes = [
        PodcastEpisode(
            **{
                "title": entry.title,
                "description": markdownify.markdownify(entry.get("description")),
                "summary": markdownify.markdownify(entry.get("summary")),
                "link": entry.link,
                "published": entry.published,
                "id": entry.id,
                "episode": entry.get("itunes_episode", "0"),
                "season": entry.get("itunes_season"),
                "cover_image": entry.get("image", {}).get("href"),
                "audio_url": entry.get("links", [{}])[1].get("href"),
            }
        )
        for entry in NewsFeed.entries
    ]

    return episodes


episodes: List[PodcastEpisode] = parse_awesome_feed(
    "https://media.rss.com/the-awesomealgo-podcast/feed.xml"
)

save_podcast_episodes_to_json(episodes, "released_episodes.json")
