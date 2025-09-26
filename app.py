from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Iterable, List

from flask import Flask, render_template, request

try:
    import snscrape.modules.twitter as sntwitter
except ModuleNotFoundError as exc:
    raise RuntimeError(
        "snscrape is required to run this application. Install dependencies via 'pip install -r requirements.txt'."
    ) from exc


app = Flask(__name__)


@dataclass
class KeywordStat:
    keyword: str
    count: int


def normalize_keyword(raw_keyword: str) -> str:
    """Normalize a keyword or hashtag provided by the user."""

    keyword = raw_keyword.strip()
    if not keyword:
        return ""

    if keyword.startswith("#"):
        keyword = keyword[1:]

    return keyword.lower()


def iter_user_tweets(username: str, limit: int = 200) -> Iterable[sntwitter.Tweet]:
    """Yield the latest tweets from a given user up to ``limit`` entries."""

    scraper = sntwitter.TwitterUserScraper(username=username, isUserId=False)
    for index, tweet in enumerate(scraper.get_items()):
        if index >= limit:
            break
        yield tweet


def count_keyword_matches(tweets: Iterable[sntwitter.Tweet], keywords: List[str]) -> Dict[str, int]:
    """Return a dictionary with match counts for each keyword."""

    normalized_keywords = [normalize_keyword(keyword) for keyword in keywords]
    normalized_keywords = [keyword for keyword in normalized_keywords if keyword]

    keyword_patterns = {
        keyword: re.compile(rf"(^|\W)#?{re.escape(keyword)}(\W|$)", re.IGNORECASE)
        for keyword in normalized_keywords
    }

    counts = {keyword: 0 for keyword in normalized_keywords}

    for tweet in tweets:
        text = tweet.rawContent or ""
        for keyword, pattern in keyword_patterns.items():
            if pattern.search(text):
                counts[keyword] += 1

    return counts


@app.route("/", methods=["GET", "POST"])
def index():
    results: List[KeywordStat] | None = None
    error: str | None = None
    total_tweets = 0

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        raw_keywords = request.form.get("keywords") or ""
        keywords = [keyword for keyword in raw_keywords.split(",") if keyword.strip()]

        if not username:
            error = "Lütfen bir kullanıcı adı girin."
        elif not keywords:
            error = "En az bir hashtag veya anahtar kelime girin."
        else:
            try:
                tweets = list(iter_user_tweets(username))
                total_tweets = len(tweets)
                if not tweets:
                    error = "Kullanıcının hiç tweeti bulunamadı." if not error else error
                else:
                    counts = count_keyword_matches(tweets, keywords)
                    results = [KeywordStat(keyword=kw, count=counts.get(kw, 0)) for kw in counts]
            except Exception as exc:  # pragma: no cover - handles network/api errors
                error = f"Veriler alınırken bir hata oluştu: {exc}"

    return render_template(
        "index.html",
        results=results,
        error=error,
        total_tweets=total_tweets,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
