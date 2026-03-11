import os
import csv
import datetime
import nltk
import pandas as pd
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

API_KEY = os.environ.get('YOUTUBE_API_KEY')
if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY environment variable not set")

SEARCH_QUERIES = [
    "Tyla singer 2025",
    "Tyla Grammy 2026",
    "Tyla Water song",
    "Tyla South Africa music",
    "Tyla new music"
]

MAX_VIDEOS_PER_QUERY = 3
MAX_COMMENTS_PER_VIDEO = 50
DATA_FILE = "data/sentiment_history.csv"
CSV_COLUMNS = [
    "collection_date", "video_id", "video_title", "comment_id",
    "comment_text", "comment_date", "like_count", "vader_compound",
    "vader_sentiment", "textblob_polarity", "textblob_subjectivity",
    "textblob_sentiment", "dual_model_agreement"
]

def get_videos(youtube, query, max_results=3):
    request = youtube.search().list(
        q=query, part="id,snippet", type="video",
        maxResults=max_results, order="date", relevanceLanguage="en"
    )
    response = request.execute()
    videos = []
    for item in response.get("items", []):
        videos.append({
            "video_id": item["id"]["videoId"],
            "video_title": item["snippet"]["title"]
        })
    return videos

def get_comments(youtube, video_id, max_results=50):
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet", videoId=video_id,
            maxResults=max_results, order="relevance", textFormat="plainText"
        )
        response = request.execute()
        for item in response.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "comment_id": item["id"],
                "comment_text": snippet["textDisplay"],
                "comment_date": snippet["publishedAt"],
                "like_count": snippet["likeCount"]
            })
    except Exception as e:
        print(f"  Could not fetch comments for {video_id}: {e}")
    return comments

def analyse_sentiment(text, vader_analyser):
    vader_scores = vader_analyser.polarity_scores(text)
    compound = vader_scores['compound']
    if compound >= 0.05:
        vader_sentiment = "positive"
    elif compound <= -0.05:
        vader_sentiment = "negative"
    else:
        vader_sentiment = "neutral"

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    if polarity > 0.05:
        textblob_sentiment = "positive"
    elif polarity < -0.05:
        textblob_sentiment = "negative"
    else:
        textblob_sentiment = "neutral"

    return {
        "vader_compound": round(compound, 4),
        "vader_sentiment": vader_sentiment,
        "textblob_polarity": round(polarity, 4),
        "textblob_subjectivity": round(subjectivity, 4),
        "textblob_sentiment": textblob_sentiment,
        "dual_model_agreement": "agree" if vader_sentiment == textblob_sentiment else "disagree"
    }

def print_summary(df, collection_date):
    new_batch = df[df['collection_date'] == collection_date]
    total = len(new_batch)
    if total == 0:
        print("No new comments collected.")
        return
    vader_counts = new_batch['vader_sentiment'].value_counts()
    positive = vader_counts.get('positive', 0)
    negative = vader_counts.get('negative', 0)
    neutral = vader_counts.get('neutral', 0)
    agreement = (new_batch['dual_model_agreement'] == 'agree').sum()
    print("\n" + "="*50)
    print(f"  TYLA SENTIMENT REPORT — {collection_date}")
    print("="*50)
    print(f"  Comments collected : {total}")
    print(f"  Videos sampled     : {new_batch['video_id'].nunique()}")
    print(f"  Positive           : {positive} ({positive/total*100:.1f}%)")
    print(f"  Neutral            : {neutral} ({neutral/total*100:.1f}%)")
    print(f"  Negative           : {negative} ({negative/total*100:.1f}%)")
    print(f"  Model agreement    : {agreement}/{total} ({agreement/total*100:.1f}%)")
    all_positive = (df['vader_sentiment'] == 'positive').sum()
    all_total = len(df)
    print(f"\n  HISTORICAL (all time)")
    print(f"  Total comments     : {all_total}")
    print(f"  Overall positive   : {all_positive/all_total*100:.1f}%")
    print("="*50 + "\n")

def main():
    collection_date = datetime.date.today().isoformat()
    print(f"\n Tyla Sentiment Tracker — Collection run: {collection_date}")
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    vader_analyser = SentimentIntensityAnalyzer()

    if os.path.exists(DATA_FILE):
        df_existing = pd.read_csv(DATA_FILE)
        existing_comment_ids = set(df_existing['comment_id'].astype(str))
        print(f"  Loaded existing data: {len(df_existing)} rows")
    else:
        df_existing = pd.DataFrame(columns=CSV_COLUMNS)
        existing_comment_ids = set()
        print("  No existing data found — starting fresh")

    new_rows = []
    seen_video_ids = set()

    for query in SEARCH_QUERIES:
        print(f"\n  Searching: '{query}'")
        try:
            videos = get_videos(youtube, query, MAX_VIDEOS_PER_QUERY)
            for video in videos:
                video_id = video['video_id']
                if video_id in seen_video_ids:
                    continue
                seen_video_ids.add(video_id)
                print(f"    {video['video_title'][:60]}...")
                comments = get_comments(youtube, video_id, MAX_COMMENTS_PER_VIDEO)
                for comment in comments:
                    if str(comment['comment_id']) in existing_comment_ids:
                        continue
                    sentiment = analyse_sentiment(comment['comment_text'], vader_analyser)
                    new_rows.append({
                        "collection_date": collection_date,
                        "video_id": video_id,
                        "video_title": video['video_title'],
                        **comment,
                        **sentiment
                    })
        except Exception as e:
            print(f"  Error with query '{query}': {e}")
            continue

    print(f"\n  New comments collected: {len(new_rows)}")
    if new_rows:
        df_new = pd.DataFrame(new_rows, columns=CSV_COLUMNS)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        os.makedirs("data", exist_ok=True)
        df_combined.to_csv(DATA_FILE, index=False)
        print(f"  Saved to {DATA_FILE} — total rows: {len(df_combined)}")
        print_summary(df_combined, collection_date)
    else:
        print("  No new comments to add.")
        if len(df_existing) > 0:
            print_summary(df_existing, df_existing['collection_date'].max())

if __name__ == "__main__":
    main()
