# podcast-show-notes

> **Audio, video, or transcript → complete podcast episode package.** Show notes, chapter timestamps, key quotes, guest bio, SEO description, social posts, newsletter blurb — all from one command.

[![PyPI](https://img.shields.io/pypi/v/podcast-show-notes?style=flat)](https://pypi.org/project/podcast-show-notes/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Quickstart

```bash
pip install podcast-show-notes

# From transcript
python -m podcast_show_notes episode.txt --podcast "My Show" --host "Alper"

# From audio (requires GOOGLE_API_KEY for Gemini transcription)
python -m podcast_show_notes episode.mp3 --podcast "My Show"

# Save show notes as markdown
python -m podcast_show_notes transcript.txt --output shownotes.md
```

## What's generated

- **Show notes** — 400-600 word narrative (not bullet spam)
- **Chapter timestamps** — named sections with descriptions  
- **Key quotes** — 3-5 memorable quotes with speaker and timestamp
- **Guest bio** — 2-3 sentences inferred from context
- **Resources** — all books, tools, URLs mentioned
- **Key takeaways** — 5-7 actionable points
- **Social** — Twitter thread, LinkedIn post, Instagram caption
- **Newsletter blurb** — 2-3 sentences for your email list
- **SEO** — meta description, keywords, episode tags

## License
MIT © [Alper Nabil Gabra Zakher](https://github.com/AlperNab)
