# Analytics and growth

Use this to read performance data, audit a channel, decide what to make more of, and fix stalled growth.

## Contents

1. The metrics that matter
2. Formulas
3. How to read a set of posts
4. Diagnosing by stage
5. Common problems and fixes
6. Running experiments
7. Channel audit
8. Growth levers
9. Reporting

## 1. The metrics that matter

| Question | Metrics |
|---|---|
| Did it reach people? | Views, reach, impressions, share of views from non-followers |
| Did the packaging work? | Hook rate or 3-second hold, click-through rate on title and thumbnail, "see more" taps |
| Did they stay? | Average percentage viewed, completion rate, average view duration, watch time |
| Did they value it? | Shares and sends, saves, comments, replies |
| Did the account grow? | Follows or subscribers gained per post, profile visits |
| Did it serve the business? | Link clicks, sign-ups, enquiries, sales, email replies |

Likes are the weakest signal. Shares and saves show value; follows per view shows whether new people want more; clicks and sign-ups show commercial effect. Total follower count is a result, not a lever.

## 2. Formulas

Use the same base for every post you compare (views for video, reach or impressions for static posts).

- **Engagement rate** = (likes + comments + shares + saves) / views or reach
- **Share rate** = shares / views or reach
- **Save rate** = saves / views or reach
- **Follow rate** = follows gained / views or reach (often shown per 1,000 views)
- **Click-through rate** = link clicks / views or reach
- **Completion rate** = full views / views
- **Average percentage viewed** = average view duration / video length
- **Follower growth rate** = net new followers / followers at the start of the period
- **Email**: open rate = opens / delivered; click rate = clicks / delivered

State which base was used. Rates calculated on followers and rates calculated on reach are not comparable.

## 3. How to read a set of posts

1. **Compare within the platform.** Numbers from different platforms mean different things; never rank a YouTube video against a Reel.
2. **Use the median, not the average.** One viral post distorts an average. The median views of the last 20 to 30 posts is the account's baseline.
3. **Find outliers both ways.** Posts at two or more times the median, and posts at half or less.
4. **Look for what the winners share**: topic, pillar, hook type, format, length, opening visual, posting slot.
5. **Group by pillar and by format** to see which combinations carry the account. Check that each group has enough posts (at least three to five) before drawing conclusions.
6. **Give posts time.** Compare posts at the same age (for example at 7 days). Search-led content keeps growing for months.
7. **Remove distortions**: paid boosts, collaborations with much larger accounts, giveaways.

The bundled script (`scripts/analyze_content.py`) does steps 2 to 5 from a CSV and flags four kinds of post:

| Flag | Meaning | What to do |
|---|---|---|
| Breakout | Reach far above the platform median | Study it; make a sequel, a deeper version and a different-format version |
| Repackage | Low reach but high share and save rates | The content is valued; the packaging failed. New hook, title or cover, then repost |
| Packaging outran content | High reach but low engagement | The hook worked; the body did not deliver. Keep the hook style, improve the payoff |
| Weak | Low reach and low engagement | Drop the topic or angle, or rethink it entirely |

## 4. Diagnosing by stage

Walk from the top and fix the first weak stage; later stages cannot be judged until earlier ones work.

| Stage | Signal | If weak, look at |
|---|---|---|
| Reach | Views against the median, non-follower share | Topic appeal, packaging, consistency of niche, account health |
| Stop | 3-second hold, click-through rate | First frame, first line, title, thumbnail |
| Stay | Average percentage viewed, completion | Pacing, length, structure, whether the hook's promise is paid |
| Value | Share and save rate, comments | Depth, usefulness, emotion, a reason to pass it on |
| Follow | Follows per 1,000 views | Clarity of the account's promise, profile, series, call to action |
| Act | Clicks, sign-ups, sales | Offer, call to action, link path, landing page |

## 5. Common problems and fixes

**Views are low on everything**
- The niche is unclear or changes from post to post. Tighten the topic for 20 to 30 posts.
- Hooks are weak or slow. Rewrite openings; test three hooks on one idea.
- Topics are of interest to the creator, not the audience. Return to audience questions and niche outliers.
- Posting is sporadic. Set a sustainable rhythm.
- Check for account problems: a notice of a guideline violation, reposted or watermarked content, banned hashtags.

**Good views, few followers**
- Content is broad or trend-led and disconnected from the account's promise.
- The profile does not say who it is for. Fix bio and pinned posts.
- No series or reason to return. Add named recurring formats and a follow call to action tied to a benefit.

**Followers but little engagement**
- The audience was gained through an old niche, giveaways or follow-for-follow. Refocus and accept slower numbers while the audience resets.
- Content has no opening for response. Ask specific questions, take positions, reply to comments.

**Engagement but no sales or leads**
- No offer content, or no clear path. Add regular offer and proof posts, one link, a simple lead magnet.
- The audience and the buyer are different people. Shift topics toward the buyer's problems.

**A sudden drop**
- Compare topics and formats before and after; a change in content is the most common cause.
- Check seasonality and whether a past period was inflated by one hit.
- Platform changes happen; respond by returning to fundamentals, not by chasing rumours about the algorithm.
- "Shadowban" is rarely the explanation. Check the account status page where the platform has one.

**Growth has plateaued**
- Raise the ceiling with new formats, collaborations, a new platform fed by repurposing, or broader-appeal topics within the niche.
- Improve packaging on proven topics.
- Remake past winners.

## 6. Running experiments

Treat changes as tests so the account learns something each month.

- **One variable at a time**: hook, length, format, topic, cover, posting time.
- **Enough attempts**: at least three to five posts per variant before judging.
- **Decide the measure first**: for example average percentage viewed for a pacing test.
- **Write it down**: hypothesis, what was changed, result, decision.

Good first tests: three hook styles on the same topic; 20-second versus 45-second versions; talking head versus voiceover with b-roll; carousel versus short video for teaching content; two thumbnail concepts on one video.

## 7. Channel audit

Structure an audit as:

1. **Snapshot**: platforms, audience size, posting frequency, goal.
2. **Profile**: name, bio, link, pinned content, visual consistency. Does a stranger understand who it is for within five seconds?
3. **Content mix**: pillars, formats, funnel stages. What is missing or overweight?
4. **Performance**: median reach, outliers, best and worst pillars and formats, retention and share and save patterns, follower trend.
5. **Packaging**: hooks, titles, covers and thumbnails across the last 20 posts.
6. **Voice and quality**: is it distinct and consistent? Production issues (audio, light, captions)?
7. **Conversion path**: calls to action, link destination, lead capture, offer visibility.
8. **Community**: reply habits, comment quality, collaborations.
9. **Recommendations**: stop, start, continue, with the top three priorities and a 30-day plan.

An audit report format is in `templates.md`.

## 8. Growth levers

In rough order of effect for most accounts:

1. A sharper niche and promise.
2. Better ideas and packaging.
3. Higher retention through tighter scripts and edits.
4. Series that bring people back.
5. Consistency over months.
6. Collaborations with accounts that share the audience.
7. Search: keywords in titles, captions and speech; evergreen how-to content.
8. Repurposing to a second platform.
9. Community: replies, comment-led content, live sessions.
10. Paid promotion of posts that already performed organically, when there is budget and a clear goal.

Give realistic expectations: growth is usually uneven, with long flat stretches and occasional jumps from single pieces. Forecast as a range from the account's own recent numbers, and show the assumptions.

## 9. Reporting

A monthly report should fit on one page and lead to decisions:

- Headline: what happened in one or two sentences.
- Key numbers against last month and against the goal.
- Top three and bottom three pieces, with the likely reason for each.
- What was learned (tests run and results).
- Next month: what to make more of, what to change, what to stop.

A report format is in `templates.md`. For clients, add the business outcomes first (leads, sales, enquiries) and platform metrics second.
