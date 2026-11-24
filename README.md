# Content Creator Lead (Claude Skill)

A skill that turns Claude into a senior content lead for creators, personal brands and businesses. It handles the whole job: strategy and positioning, ideas and hooks, video scripts, titles and thumbnails, captions, carousels, threads, newsletters, repurposing, content calendars, team briefs, performance analysis, growth, and brand deals.

## What it does

| Area | Examples |
|---|---|
| Strategy | Niche and audience, positioning statement, content pillars, voice guide, 90-day plan sized to your hours |
| Ideas and hooks | Idea banks grouped by pillar, angles from one topic, hook options, series concepts, competitor research method |
| Video | Short video scripts in a film-ready table, long video outlines, retention techniques, titles, thumbnail briefs |
| Writing | Captions, carousels slide by slide, LinkedIn and X posts, threads, newsletters, search-led blog posts |
| Repurposing | One long piece turned into a pack of clips, carousels, posts and a newsletter |
| Platforms | Instagram, TikTok, YouTube and Shorts, LinkedIn, X, Threads, Facebook, Pinterest, podcast, newsletter |
| Calendar and production | Dated content calendars, batching routine, production pipeline, launch calendars |
| Team lead | Briefs for editors, designers and writers, feedback on drafts, checklists, delegation order |
| Analytics and growth | Channel audits, what to make more of, stalled-growth diagnosis, experiments, monthly reports |
| Monetization | Sponsorship pricing, media kit, brand pitches, UGC work, product ideas, disclosure rules |
| Data analysis | A bundled script reads a CSV of your posts and flags what to repeat, repackage and drop |

## Install

### Claude apps (claude.ai, desktop, mobile)

1. Download [`dist/content-creator-lead.zip`](dist/content-creator-lead.zip) (or the identical `.skill` file) from this repository, or zip the `content-creator-lead` folder yourself.
2. In Claude, open **Settings → Capabilities → Skills** and upload the file.
3. Switch the skill on. Code execution must be enabled for skills to work.

### Claude Code

Copy the skill folder into your skills directory:

```bash
git clone https://github.com/rana537omar/content-creator-lead-skill.git
cp -r content-creator-lead-skill/content-creator-lead ~/.claude/skills/
```

Use `.claude/skills/` inside a project instead if you want it for that project only.

## Use

Just ask. The skill loads on its own when a request is about content. Examples:

- "I'm a fitness coach for busy dads with 5 hours a week and no followers. Build my content strategy."
- "Give me 20 video ideas with hooks for a home bakery."
- "Write a 40-second Reel script about why most budgets fail, with three hook options."
- "Plan my content calendar for next month, starting on the 1st: Instagram and LinkedIn."
- "Turn this podcast transcript into 5 short videos, a carousel and a newsletter."
- "Here are my posts from the last two months. What should I make more of?" (attach the CSV)
- "A skincare brand wants one Reel and three stories. What should I charge, and how do I reply?"
- "Review this script and tell me what to fix."
- "Write a brief for my video editor for this week's clips."

### Tracking posts for analysis

Keep one row per post in a spreadsheet and export it as CSV. Useful columns: `date, platform, format, pillar, title, views, likes, comments, shares, saves, clicks, follows, retention`. Common alternative names from platform exports are recognised (for example reach or impressions in place of views).

The analyzer can also be run on its own (Python 3, no dependencies):

```bash
python content-creator-lead/scripts/analyze_content.py examples/sample-posts.csv
python content-creator-lead/scripts/analyze_content.py examples/sample-posts.csv --platform instagram --by pillar,format
```

## Contents

```
content-creator-lead/
├── SKILL.md                              Core workflow and operating principles
├── references/
│   ├── strategy-and-positioning.md       Niche, audience, pillars, voice, 90-day plan
│   ├── ideas-and-hooks.md                Idea sources, angles, hook patterns, research
│   ├── video-scripts-and-packaging.md    Short and long video, titles, thumbnails
│   ├── written-content.md                Captions, carousels, posts, newsletters, blogs, repurposing
│   ├── platform-playbooks.md             Platform notes, profiles, keywords, timing, community
│   ├── calendar-and-production.md        Calendars, batching, pipeline, briefs, team
│   ├── analytics-and-growth.md           Metrics, diagnosis, audits, experiments, reporting
│   ├── monetization-and-brand-deals.md   Income streams, pricing, media kit, disclosure
│   └── templates.md                      Intake, strategy page, script sheets, briefs, reports
├── scripts/
│   └── analyze_content.py                Post performance CSV analyzer
└── evals/                                Test cases used to check the skill
examples/
└── sample-posts.csv                      Sample data for trying the analyzer
```

## Notes

- The skill gives strategy, writing and analysis. It does not connect to a social account by itself. If you give Claude tools that can post or reply on a live account, the skill instructs it to show you what will go out and confirm first.
- Platforms change features, limits and ranking often. Confirm specifics such as length limits, specs and monetization thresholds in each platform's help pages.
- Results depend on your niche, ideas, consistency and audience. Nothing here guarantees views, followers or income.
- The skill will not help with bought followers or engagement, fake reviews, hidden sponsorships, copied content or misleading claims.
- Pricing and legal notes are general guidance, not legal or tax advice.
- Not affiliated with or endorsed by any social media platform.

## License

MIT. See [LICENSE](LICENSE).
