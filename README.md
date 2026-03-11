# 🎵 Tyla Sentiment Tracker — AZ-400 DevOps Portfolio

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![YouTube API](https://img.shields.io/badge/YouTube%20Data%20API%20v3-FF0000?style=for-the-badge&logo=youtube&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK%20%7C%20VADER-3776AB?style=for-the-badge&logo=python&logoColor=white)

> Automated fortnightly sentiment tracking pipeline for South African artist Tyla —
> collecting and analysing YouTube comment sentiment every 2 weeks using
> VADER and TextBlob dual-model analysis, building a longitudinal dataset
> across her 2026 career arc.

---

## 📋 Table of Contents

- [Purpose](#purpose)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [The Data](#the-data)
- [Technologies](#technologies)
- [How to Run](#how-to-run)
- [Pipeline](#pipeline)
- [Connection to Original Project](#connection-to-original-project)
- [Credits](#credits)

---

## 💼 Purpose

South African artist Tyla made history at the 2024 and 2026 Grammy Awards,
bringing her "Popiano" sound to global audiences. Public sentiment around her
has been complex — celebrated internationally while simultaneously facing
criticism about her heritage and identity from certain voices online.

This project answers a question no static analysis can:

> **How is sentiment around Tyla evolving over time?**

By running automatically every 2 weeks, this pipeline builds a longitudinal
dataset that tracks sentiment shifts in response to real-world events —
new music releases, awards, controversies, and cultural moments.

**For prospective brand partners and stakeholders, this dataset provides:**

| Question | Answer |
|---|---|
| Is positive sentiment sustained or was it a Grammy spike? | Tracked fortnightly |
| How do controversies affect public perception? | Visible in the data |
| Which moments drive the most engagement? | Captured by volume |
| Is her audience growing or plateauing? | Shown by comment trends |

---

## ⚙️ How It Works
```
Every 2 weeks (1st and 15th of each month):

  GitHub Actions wakes up
       │
       ▼
  Searches YouTube for recent Tyla content
  (5 search queries × 3 videos × 50 comments)
       │
       ▼
  Runs VADER + TextBlob dual sentiment analysis
  on every new comment
       │
       ▼
  Appends results to data/sentiment_history.csv
  (never overwrites — always appends)
       │
       ▼
  Commits updated CSV back to this repo
  Saves CSV as downloadable artifact (90 days)
       │
       ▼
  Prints sentiment summary to pipeline logs
```

---

## 📁 Project Structure
```
Tyla-Sentiment-Tracker/
├── .github/
│   └── workflows/
│       └── sentiment-tracker.yml   # Scheduled pipeline — runs every 2 weeks
├── scripts/
│   └── collect_and_analyse.py      # Core script — fetches + analyses
├── data/
│   └── sentiment_history.csv       # Grows with every run (auto-committed)
├── requirements.txt                # Python dependencies
└── README.md
```

---

## 📊 The Data

Each row in `sentiment_history.csv` represents one YouTube comment:

| Column | Description |
|---|---|
| `collection_date` | Date this comment was collected |
| `video_id` | YouTube video ID |
| `video_title` | Title of the video |
| `comment_id` | Unique YouTube comment ID |
| `comment_text` | Raw comment text |
| `comment_date` | When the comment was posted |
| `like_count` | Number of likes on the comment |
| `vader_compound` | VADER compound score (-1 to +1) |
| `vader_sentiment` | positive / neutral / negative |
| `textblob_polarity` | TextBlob polarity score (-1 to +1) |
| `textblob_subjectivity` | TextBlob subjectivity (0 to 1) |
| `textblob_sentiment` | positive / neutral / negative |
| `dual_model_agreement` | agree / disagree between models |

### Duplicate prevention
Comments already in the CSV are never re-added. Each run only
appends genuinely new comments — keeping the dataset clean.

---

## 🛠️ Technologies

**Pipeline & Automation**

![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

**Data Collection**

![YouTube API](https://img.shields.io/badge/YouTube%20Data%20API%20v3-FF0000?style=for-the-badge&logo=youtube&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**Sentiment Analysis**

![NLTK](https://img.shields.io/badge/VADER-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TextBlob](https://img.shields.io/badge/TextBlob-FF6F00?style=for-the-badge&logo=python&logoColor=white)

**Data Storage**

![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![CSV](https://img.shields.io/badge/CSV-217346?style=for-the-badge&logo=files&logoColor=white)

| Category | Tools |
|---|---|
| **Automation** | GitHub Actions, cron schedule |
| **Data Collection** | YouTube Data API v3 |
| **Sentiment Analysis** | VADER, TextBlob |
| **Data Processing** | Pandas, NumPy, NLTK |
| **Storage** | CSV, GitHub Artifacts |

---

## ⚙️ How to Run

### Automatic
The pipeline runs automatically on the **1st and 15th of every month**.
No action needed — just check the Actions tab to see results.

### Manual trigger
1. Go to **Actions** tab
2. Click **Tyla Sentiment Tracker**
3. Click **Run workflow**
4. Optionally add a reason (e.g. "Tyla dropped new album")
5. Click **Run workflow**

### Download the CSV
1. Go to **Actions** tab
2. Click any completed run
3. Scroll to **Artifacts**
4. Download `tyla-sentiment-data-{run_number}`

### Local setup
```bash
# Clone the repo
git clone https://github.com/AZ400-DevOps-Portfolio/Tyla-Sentiment-Tracker.git
cd Tyla-Sentiment-Tracker

# Install dependencies
pip install -r requirements.txt

# Set your YouTube API key
export YOUTUBE_API_KEY="your_api_key_here"

# Run manually
python scripts/collect_and_analyse.py
```

---

## 🔄 Pipeline

| Job | What it does |
|---|---|
| Collect & Analyse Sentiment | Fetches YouTube comments, runs dual sentiment analysis, appends to CSV |
| Collection Summary | Prints sentiment breakdown and historical trend to pipeline logs |

**Schedule:** 1st and 15th of every month at 8am SAST

---

## 🔗 Connection to Original Project

This tracker is a **DevOps extension** of the original data science project:

👉 [Tyla-Grammy-NLP-Analysis](https://github.com/Lindiwe-22/Tyla-Grammy-NLP-Analysis)

| Original Project | This Tracker |
|---|---|
| Static snapshot — Grammy moment | Living dataset — ongoing tracking |
| Manual data collection | Fully automated pipeline |
| One-time analysis | Longitudinal trend analysis |
| Jupyter notebook | Production Python script |

The same VADER + TextBlob dual-model methodology is used in both projects,
meaning results are directly comparable — you can see exactly how sentiment
has shifted since the Grammy wins.

---

## 🔐 Setup for Forking

To run this pipeline in your own GitHub account:

1. Fork this repository
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Add a secret: `YOUTUBE_API_KEY` = your YouTube Data API v3 key
4. Go to **Actions** tab and enable workflows
5. Trigger a manual run to test

---

## 🙏 Credits

**Developed by Lindiwe Songelwa — Data Scientist | DevOps Engineer | Insight Creator**

| Platform | Link |
|---|---|
| 💼 LinkedIn | [Lindiwe S.](https://www.linkedin.com/in/lindiwe-songelwa) |
| 🌐 Portfolio | [Creative Portfolio](https://lindiwe-22.github.io/Portfolio-Website/) |
| 🏅 Credly | [Lindiwe Songelwa – Badges](https://www.credly.com/users/samnkelisiwe-lindiwe-songelwa) |
| 🔬 Original Project | [Tyla Grammy NLP Analysis](https://github.com/Lindiwe-22/Tyla-Grammy-NLP-Analysis) |
| 📧 Email | [sl.songelwa@hotmail.co.za](mailto:sl.songelwa@hotmail.co.za) |

---

*© 2026 Lindiwe Songelwa. All rights reserved.*
