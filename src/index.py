#!/usr/bin/env python3
"""
podcast-show-notes — audio/transcript → complete episode package
Generates: show notes, chapter timestamps, key quotes, guest bio,
episode summary, SEO description, social posts, newsletter blurb
"""
import anthropic, base64, json, os, re, sys
from pathlib import Path

SYSTEM = """You are a professional podcast producer and content strategist.
Create a complete episode content package from the provided audio/transcript.

Return ONLY valid JSON — no markdown, no explanation.

{
  "episode_title": "compelling episode title (not just guest name)",
  "subtitle": "subtitle or episode tagline",
  "summary": "2-3 sentence episode summary",
  "detailed_show_notes": "400-600 word show notes in markdown format — narrative style, not bullet spam",
  "chapters": [
    {
      "timestamp": "00:00",
      "title": "chapter title",
      "description": "1 sentence what happens in this section"
    }
  ],
  "key_quotes": [
    {
      "speaker": "name or 'Host'",
      "quote": "exact memorable quote under 60 words",
      "timestamp": "00:00 or null",
      "context": "brief context for the quote"
    }
  ],
  "guest": {
    "name": "string or null",
    "title": "string or null",
    "bio": "2-3 sentence guest bio from context clues",
    "links_mentioned": ["list of URLs or resources the guest mentioned"]
  },
  "resources_mentioned": [
    {"title":"string","url":"string or null","type":"book|tool|website|person|concept"}
  ],
  "key_takeaways": ["5-7 actionable takeaways from the episode"],
  "seo": {
    "meta_description": "under 155 chars",
    "keywords": ["5-8 search keywords"],
    "episode_tags": ["podcast tags"]
  },
  "social": {
    "twitter_thread": ["tweet 1","tweet 2","tweet 3"],
    "linkedin_post": "150 word professional post",
    "instagram_caption": "caption with hashtags",
    "newsletter_blurb": "2-3 sentences for an email newsletter"
  },
  "call_to_action": "suggested CTA for the episode",
  "next_episode_hook": "teaser line to keep listeners coming back",
  "transcript_excerpt": "most compelling 100-word excerpt for embedding"
}"""

def process(source: str, podcast_name: str = "", host_name: str = "") -> dict:
    client = anthropic.Anthropic()
    path = Path(source) if source != "-" else None

    context = []
    if podcast_name: context.append(f"Podcast: {podcast_name}")
    if host_name: context.append(f"Host: {host_name}")
    ctx = "\n".join(context)

    if path and path.exists():
        suffix = path.suffix.lower()
        audio_exts = {".mp3","audio/mpeg",".wav",".m4a",".ogg",".flac",".aac"}
        video_exts = {".mp4",".mov",".webm"}
        text_exts = {".txt",".md",".srt",".vtt"}

        if suffix in text_exts:
            text = path.read_text(encoding="utf-8", errors="replace")[:50000]
            prompt = f"{ctx}\n\nCreate episode package from this transcript:\n\n{text}"
            msgs = [{"role":"user","content":prompt}]

        elif suffix in audio_exts or suffix in video_exts:
            # Use Gemini if available, otherwise Claude
            google_key = os.environ.get("GOOGLE_API_KEY","")
            if google_key:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=google_key)
                    mime_map = {".mp3":"audio/mpeg",".wav":"audio/wav",".m4a":"audio/mp4",
                               ".ogg":"audio/ogg",".flac":"audio/flac",".aac":"audio/aac",
                               ".mp4":"video/mp4",".mov":"video/quicktime",".webm":"video/webm"}
                    mime = mime_map.get(suffix,"audio/mpeg")
                    data = base64.standard_b64encode(path.read_bytes()).decode("ascii")
                    model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
                    trans_resp = model.generate_content([
                        {"inline_data":{"mime_type":mime,"data":data}},
                        "Transcribe this podcast episode completely with speaker labels and timestamps."
                    ])
                    transcript = trans_resp.text
                    prompt = f"{ctx}\n\nCreate episode package from this transcript:\n\n{transcript[:50000]}"
                    msgs = [{"role":"user","content":prompt}]
                except Exception as e:
                    print(f"Gemini failed ({e}), falling back to Claude", file=sys.stderr)
                    data = base64.standard_b64encode(path.read_bytes()).decode("ascii")
                    mime = {".mp4":"video/mp4",".mov":"video/quicktime",".webm":"video/webm"}.get(suffix,"video/mp4")
                    msgs = [{"role":"user","content":[
                        {"type":"document","source":{"type":"base64","media_type":mime,"data":data}},
                        {"type":"text","text":f"{ctx}\n\nCreate complete episode package."}
                    ]}]
            else:
                data = base64.standard_b64encode(path.read_bytes()).decode("ascii")
                mime = {".mp4":"video/mp4",".mov":"video/quicktime",".webm":"video/webm"}.get(suffix,"video/mp4")
                msgs = [{"role":"user","content":[
                    {"type":"document","source":{"type":"base64","media_type":mime,"data":data}},
                    {"type":"text","text":f"{ctx}\n\nCreate complete episode package."}
                ]}]
        else:
            text = path.read_text(encoding="utf-8", errors="replace")[:50000]
            msgs = [{"role":"user","content":f"{ctx}\n\nCreate episode package:\n\n{text}"}]
    else:
        text = (sys.stdin.read() if source=="-" else source)[:50000]
        msgs = [{"role":"user","content":f"{ctx}\n\nCreate episode package:\n\n{text}"}]

    resp = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=4096, system=SYSTEM,
        messages=msgs
    )
    raw = re.sub(r'^```(?:json)?\s*','',resp.content[0].text.strip(),flags=re.MULTILINE)
    raw = re.sub(r'\s*```$','',raw,flags=re.MULTILINE)
    return json.loads(raw)

def print_package(r: dict):
    print(f"\n{'═'*60}")
    print(f"  {r.get('episode_title','Episode')}")
    print(f"  {r.get('subtitle','')}")
    print(f"{'═'*60}")
    print(f"\n  {r.get('summary','')}")

    chapters = r.get("chapters",[])
    if chapters:
        print(f"\n  CHAPTERS ({len(chapters)})")
        for c in chapters: print(f"  {c.get('timestamp','00:00')}  {c.get('title','')}")

    quotes = r.get("key_quotes",[])
    if quotes:
        print(f"\n  KEY QUOTES")
        for q in quotes[:3]:
            print(f"\n  \"{q.get('quote','')}\"")
            print(f"  — {q.get('speaker','?')} {('@ '+q['timestamp']) if q.get('timestamp') else ''}")

    takeaways = r.get("key_takeaways",[])
    if takeaways:
        print(f"\n  KEY TAKEAWAYS")
        for t in takeaways: print(f"  • {t}")

    resources = r.get("resources_mentioned",[])
    if resources:
        print(f"\n  RESOURCES MENTIONED")
        for res in resources:
            url = f" — {res['url']}" if res.get("url") else ""
            print(f"  • {res.get('title','')}{url}")

    social = r.get("social",{})
    if social.get("newsletter_blurb"):
        print(f"\n  NEWSLETTER BLURB\n  {social['newsletter_blurb']}")

    print(f"\n  CTA: {r.get('call_to_action','')}")
    print(f"{'═'*60}\n")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Generate podcast show notes and episode package")
    p.add_argument("input", help="Audio file, transcript .txt, or '-' for stdin")
    p.add_argument("--podcast", default="", help="Podcast name")
    p.add_argument("--host", default="", help="Host name")
    p.add_argument("--json", action="store_true")
    p.add_argument("--output", "-o", help="Save show notes to file")
    a = p.parse_args()
    r = process(a.input, a.podcast, a.host)
    if a.output:
        Path(a.output).write_text(r.get("detailed_show_notes",""), encoding="utf-8")
        print(f"Show notes saved to {a.output}")
    if a.json: print(json.dumps(r, indent=2, ensure_ascii=False))
    else: print_package(r)
