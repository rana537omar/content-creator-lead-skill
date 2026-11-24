#!/usr/bin/env python3
"""Analyze a content performance export or tracker (CSV).

Reads one row per post, calculates engagement, share, save and follow rates,
summarises by platform, format, pillar and weekday, and flags posts worth
repeating, repackaging or dropping.

Usage:
    python analyze_content.py posts.csv
    python analyze_content.py posts.csv --by pillar,format --top 5
    python analyze_content.py posts.csv --platform instagram

No dependencies beyond the Python 3 standard library.
"""

import argparse
import csv
import statistics
import sys
from collections import defaultdict
from datetime import datetime

ALIASES = {
    "date": ["date", "published", "publish date", "post date", "posted", "date posted",
             "publish time", "video publish time", "post time", "created", "created time", "time"],
    "platform": ["platform", "channel", "network", "account"],
    "format": ["format", "type", "post type", "content type", "media type"],
    "pillar": ["pillar", "content pillar", "topic", "category", "theme", "series"],
    "title": ["title", "hook", "video title", "post title", "caption", "description",
              "post", "text", "post text", "content", "name", "permalink"],
    "views": ["views", "video views", "plays", "view count"],
    "impressions": ["impressions"],
    "reach": ["reach", "accounts reached", "people reached"],
    "likes": ["likes", "reactions", "like count", "favorites"],
    "comments": ["comments", "replies", "comment count", "comments added"],
    "shares": ["shares", "reposts", "retweets", "sends", "share count"],
    "saves": ["saves", "bookmarks", "saved"],
    "clicks": ["clicks", "link clicks", "website clicks", "url clicks"],
    "follows": ["follows", "new followers", "followers gained", "new follows",
                "subscribers", "subscribers gained", "new subscribers"],
    "retention": ["retention", "retention %", "retention rate", "avg % viewed",
                  "average percentage viewed", "average percentage viewed (%)",
                  "avg view percentage", "completion rate", "watched full video"],
}

DATE_FORMATS = [
    "%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%d.%m.%Y",
    "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y %H:%M",
    "%m/%d/%Y %H:%M", "%b %d, %Y", "%d %b %Y", "%B %d, %Y", "%d %B %Y",
]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DIMENSIONS = ["platform", "format", "pillar", "weekday"]


def norm(text):
    return " ".join(str(text).replace("﻿", "").replace("_", " ").replace("-", " ").lower().split())


def map_columns(header):
    """Return {field: column name} for the fields found in the header."""
    lookup = {norm(col): col for col in header if col is not None}
    found = {}
    for field, names in ALIASES.items():
        for name in names:
            if name in lookup:
                found[field] = lookup[name]
                break
    return found


def to_number(value):
    """Parse '1,234', '12.5%', '3.4K', '1.2M'. Returns None for blanks."""
    if value is None:
        return None
    text = str(value).strip().replace(",", "").replace("%", "").replace(" ", "")
    if text in ("", "-", "--", "n/a", "N/A", "na", "null", "None"):
        return None
    mult = 1.0
    if text[-1] in "kK":
        mult, text = 1e3, text[:-1]
    elif text[-1] in "mM":
        mult, text = 1e6, text[:-1]
    try:
        return float(text) * mult
    except ValueError:
        return None


def to_date(value):
    if not value:
        return None
    text = str(value).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(handle, dialect=dialect)
        columns = map_columns(reader.fieldnames or [])
        posts = []
        for raw in reader:
            post = {}
            for field in ("platform", "format", "pillar", "title"):
                value = (raw.get(columns[field]) or "").strip() if field in columns else ""
                post[field] = value
            for field in ("views", "impressions", "reach", "likes", "comments", "shares",
                          "saves", "clicks", "follows", "retention"):
                post[field] = to_number(raw.get(columns[field])) if field in columns else None
            when = to_date(raw.get(columns["date"])) if "date" in columns else None
            post["date"] = when
            post["weekday"] = WEEKDAYS[when.weekday()] if when else ""
            base = next((post[k] for k in ("views", "impressions", "reach") if post[k]), None)
            if not base:
                continue  # no reach figure: cannot compare this row
            post["base"] = base
            post["eng"] = sum(post[k] or 0 for k in ("likes", "comments", "shares", "saves"))
            post["er"] = post["eng"] / base
            post["value"] = ((post["shares"] or 0) + (post["saves"] or 0)) / base
            if not post["platform"]:
                post["platform"] = "(all)"
            posts.append(post)
    return posts, columns


def pct(value):
    return "-" if value is None else f"{value * 100:.1f}%"


def num(value):
    if value is None:
        return "-"
    if value >= 1e6:
        return f"{value / 1e6:.1f}M"
    if value >= 1e4:
        return f"{value / 1e3:.0f}K"
    if value >= 1e3:
        return f"{value / 1e3:.1f}K"
    return f"{value:.0f}"


def rate(posts, field):
    """Reach-weighted rate for a field across posts; None if never recorded."""
    rows = [p for p in posts if p[field] is not None]
    if not rows:
        return None
    return sum(p[field] for p in rows) / sum(p["base"] for p in rows)


def summarise(posts, all_follows=0):
    retention = [p["retention"] for p in posts if p["retention"] is not None]
    follows = rate(posts, "follows")
    return {
        "n": len(posts),
        "median": statistics.median(p["base"] for p in posts),
        "total": sum(p["base"] for p in posts),
        "er": sum(p["eng"] for p in posts) / sum(p["base"] for p in posts),
        "share": rate(posts, "shares"),
        "save": rate(posts, "saves"),
        "follows_per_k": None if follows is None else follows * 1000,
        "follow_share": (sum(p["follows"] or 0 for p in posts) / all_follows) if all_follows else None,
        "click": rate(posts, "clicks"),
        "retention": statistics.mean(retention) if retention else None,
    }


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(out)


def summary_row(label, s, min_posts):
    note = " *" if s["n"] < min_posts else ""
    retention = "-" if s["retention"] is None else f"{s['retention']:.0f}%"
    follows = "-" if s["follows_per_k"] is None else f"{s['follows_per_k']:.1f}"
    follow_share = "-" if s["follow_share"] is None else f"{s['follow_share'] * 100:.0f}%"
    click = "-" if s["click"] is None else f"{s['click'] * 100:.2f}%"
    return [label + note, s["n"], num(s["median"]), num(s["total"]), pct(s["er"]),
            pct(s["share"]), pct(s["save"]), click, follows, follow_share, retention]


SUMMARY_HEADERS = ["", "Posts", "Median reach", "Total reach", "Eng. rate",
                   "Share rate", "Save rate", "Click rate", "Follows /1K", "% of follows", "Avg % viewed"]


def short(text, limit=60):
    text = " ".join((text or "(untitled)").split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def post_row(p, baseline):
    ratio = p["base"] / baseline if baseline else 0
    when = p["date"].strftime("%Y-%m-%d") if p["date"] else "-"
    return [when, short(p["title"]), p["format"] or "-", p["pillar"] or "-", num(p["base"]),
            f"{ratio:.1f}x", pct(p["er"]), pct(p["value"]),
            "-" if p["clicks"] is None else f"{p['clicks'] / p['base'] * 100:.2f}%",
            "-" if p["follows"] is None else f"{p['follows']:.0f}"]


POST_HEADERS = ["Date", "Post", "Format", "Pillar", "Reach", "vs median", "Eng. rate", "Share+save", "Click rate", "Follows"]


def flag_posts(posts):
    """Classify posts against their platform's median reach and rates."""
    flags = {"breakout": [], "repackage": [], "outran": [], "weak": []}
    base_med = statistics.median(p["base"] for p in posts)
    er_med = statistics.median(p["er"] for p in posts)
    value_med = statistics.median(p["value"] for p in posts)
    for p in posts:
        reach_x = p["base"] / base_med if base_med else 0
        er_x = p["er"] / er_med if er_med else 0
        value_x = p["value"] / value_med if value_med else 0
        if reach_x >= 2 and er_x > 0.6:
            flags["breakout"].append(p)
        if reach_x <= 0.6 and value_x >= 1.5 and value_med > 0:
            flags["repackage"].append(p)
        elif reach_x <= 0.5 and er_x <= 0.7:
            flags["weak"].append(p)
        if reach_x >= 1.5 and er_x <= 0.6:
            flags["outran"].append(p)
    for group in flags.values():
        group.sort(key=lambda p: p["base"], reverse=True)
    return flags, base_med


FLAG_TEXT = [
    ("breakout", "Breakout: reach at least 2x the median, with engagement to match",
     "Study the topic, hook and format. Make a sequel, a deeper version and a different-format version."),
    ("repackage", "Repackage: low reach, but the people who saw it shared and saved it",
     "The content is valued and the packaging failed. Give it a new hook, title or cover and post it again."),
    ("outran", "Packaging outran content: high reach, low engagement",
     "The hook worked and the body did not deliver. Keep the hook style and strengthen the payoff."),
    ("weak", "Weak: low reach and low engagement",
     "Drop this topic or angle, or rethink it from the audience's side."),
]


def report(posts, columns, dims, top, min_posts):
    lines = ["# Content performance analysis", ""]
    dates = [p["date"] for p in posts if p["date"]]
    period = f", {min(dates):%Y-%m-%d} to {max(dates):%Y-%m-%d}" if dates else ""
    lines.append(f"{len(posts)} posts analysed{period}.")
    base_cols = [k for k in ("views", "impressions", "reach") if k in columns]
    lines.append(f"Reach base per post: first available of {', '.join(base_cols)}. "
                 "Rates are reach-weighted. Compare posts within a platform, not across platforms.")
    missing = [k for k in ("shares", "saves", "follows", "retention", "pillar", "format") if k not in columns]
    if missing:
        lines.append(f"Columns not found (add them for a fuller picture): {', '.join(missing)}.")
    lines.append("")

    for dim in dims:
        groups = defaultdict(list)
        for p in posts:
            if p[dim]:
                groups[p[dim]].append(p)
        if len(groups) < 2 and dim != "platform":
            continue
        if not groups:
            continue
        lines.append(f"## By {dim}")
        lines.append("")
        if dim == "weekday":
            keys = [d for d in WEEKDAYS if d in groups]
        else:
            keys = sorted(groups, key=lambda k: statistics.median(p["base"] for p in groups[k]), reverse=True)
        all_follows = sum(p["follows"] or 0 for p in posts)
        rows = [summary_row(k, summarise(groups[k], all_follows), min_posts) for k in keys]
        lines.append(table([dim.capitalize()] + SUMMARY_HEADERS[1:], rows))
        if any(len(groups[k]) < min_posts for k in keys):
            lines.append("")
            lines.append(f"\\* fewer than {min_posts} posts: too few to draw a conclusion.")
        if dim == "weekday":
            lines.append("")
            lines.append("Weekday results are easily skewed by which topics happened to land on which day. "
                         "Treat them as a hint to test, not a finding.")
        if dim != "platform" and len({p["platform"] for p in posts}) > 1:
            lines.append("")
            lines.append("Note: this table mixes platforms. Use --platform to view one at a time.")
        lines.append("")

    by_platform = defaultdict(list)
    for p in posts:
        by_platform[p["platform"]].append(p)

    for platform in sorted(by_platform, key=lambda k: len(by_platform[k]), reverse=True):
        rows = by_platform[platform]
        lines.append(f"## Posts: {platform}")
        lines.append("")
        median = statistics.median(p["base"] for p in rows)
        lines.append(f"{len(rows)} posts, median reach {num(median)}.")
        lines.append("")
        ranked = sorted(rows, key=lambda p: p["base"], reverse=True)
        n = min(top, max(1, len(ranked) // 2))
        lines.append(f"**Top {n} by reach**")
        lines.append("")
        lines.append(table(POST_HEADERS, [post_row(p, median) for p in ranked[:n]]))
        lines.append("")
        if len(ranked) > n:
            lines.append(f"**Bottom {n} by reach**")
            lines.append("")
            lines.append(table(POST_HEADERS, [post_row(p, median) for p in ranked[-n:]]))
            lines.append("")
        if len(rows) < 5:
            lines.append("Fewer than 5 posts on this platform: not enough to flag patterns.")
            lines.append("")
            continue
        flags, _ = flag_posts(rows)
        any_flag = False
        for key, title, advice in FLAG_TEXT:
            if not flags[key]:
                continue
            any_flag = True
            lines.append(f"**{title}**")
            lines.append("")
            lines.append(table(POST_HEADERS, [post_row(p, median) for p in flags[key][:top]]))
            lines.append("")
            lines.append(advice)
            lines.append("")
        if not any_flag:
            lines.append("No posts stand out strongly in either direction on this platform.")
            lines.append("")

    lines.append("## Reading this report")
    lines.append("")
    lines.append("- Flags are relative to each platform's own median, so they describe this account, not an industry benchmark.")
    lines.append("- Check post age, paid boosts, collaborations and trends before acting on a single post.")
    lines.append("- A pattern needs several posts. One hit or one flop is a lead to test, not a conclusion.")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze a content performance CSV: one row per post.",
        epilog="Recognised columns (any order, common alternative names accepted): date, platform, "
               "format, pillar, title, views / impressions / reach, likes, comments, shares, saves, "
               "clicks, follows, retention.")
    parser.add_argument("csv_file", help="path to the CSV export or tracker")
    parser.add_argument("--by", default="platform,format,pillar,weekday",
                        help="comma-separated breakdowns: platform, format, pillar, weekday (default: all)")
    parser.add_argument("--platform", help="only analyse posts from this platform (case-insensitive)")
    parser.add_argument("--top", type=int, default=5, help="posts to list in each ranking (default 5)")
    parser.add_argument("--min-posts", type=int, default=3,
                        help="groups with fewer posts are marked as too small (default 3)")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    try:
        posts, columns = load(args.csv_file)
    except FileNotFoundError:
        sys.exit(f"File not found: {args.csv_file}")
    except UnicodeDecodeError:
        sys.exit("Could not read the file as UTF-8. Re-save it as 'CSV UTF-8' and try again.")

    if not any(k in columns for k in ("views", "impressions", "reach")):
        sys.exit("No views, impressions or reach column found. Columns seen map to: "
                 + (", ".join(sorted(columns)) or "none")
                 + ". Add a views or reach column with one row per post.")
    if args.platform:
        posts = [p for p in posts if p["platform"].lower() == args.platform.lower()]
    if not posts:
        sys.exit("No rows with a views or reach figure to analyse.")

    dims = [d.strip().lower() for d in args.by.split(",") if d.strip()]
    unknown = [d for d in dims if d not in DIMENSIONS]
    if unknown:
        sys.exit(f"Unknown breakdown: {', '.join(unknown)}. Choose from {', '.join(DIMENSIONS)}.")

    print(report(posts, columns, dims, max(1, args.top), max(1, args.min_posts)))


if __name__ == "__main__":
    main()
