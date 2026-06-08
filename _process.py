#!/usr/bin/env python3
"""Process AIHot API data for suduai.top site update."""
import json, os, re, html
from datetime import datetime, timezone, timedelta

TODAY = "2026-06-08"
BJT = timezone(timedelta(hours=8))

def load_api():
    with open('aihot_selected.json', 'r') as f:
        return json.load(f)['items']

def fmt_time(iso_str):
    """Convert ISO time to BJT display format."""
    if not iso_str:
        return ""
    try:
        dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        dt_bjt = dt.astimezone(BJT)
        today_dt = datetime.strptime(TODAY, "%Y-%m-%d").replace(tzinfo=BJT)
        yesterday_dt = today_dt - timedelta(days=1)
        
        if dt_bjt.date() == today_dt.date():
            return f"今天 {dt_bjt.strftime('%H:%M')}"
        elif dt_bjt.date() == yesterday_dt.date():
            return f"昨天 {dt_bjt.strftime('%H:%M')}"
        else:
            return dt_bjt.strftime('%m/%d %H:%M')
    except:
        return ""

def clean_source(source):
    """Clean source name: remove X: prefix, parenthetical notes, truncate to 18 chars."""
    if not source:
        return ""
    s = source.strip()
    # Remove X： or X: prefix
    s = re.sub(r'^X[:：：]\s*', '', s)
    # Remove parenthetical content like (@username), (RSS), etc
    s = re.sub(r'[（(][^)）]*[)）]', '', s).strip()
    if len(s) > 18:
        s = s[:15] + '...'
    return s

def cat_mapping(api_cat):
    """Map API category to data-category attribute."""
    mapping = {
        'ai-models': 'ai-models',
        'ai-products': 'ai-products',
        'industry': 'industry',
        'paper': 'paper',
        'tip': 'tip'
    }
    return mapping.get(api_cat, 'tip')

def cat_label(api_cat):
    """Map API category to display label."""
    mapping = {
        'ai-models': '模型',
        'ai-products': '产品',
        'industry': '行业',
        'paper': '论文',
        'tip': '技巧'
    }
    return mapping.get(api_cat, '技巧')

def cat_daily_icon(api_cat):
    icons = {
        'ai-models': '🤖',
        'ai-products': '🚀',
        'industry': '🏭',
        'paper': '📄',
        'tip': '💡'
    }
    return icons.get(api_cat, '📌')

def cat_daily_title(api_cat):
    titles = {
        'ai-models': '模型发布/更新',
        'ai-products': '产品发布/更新',
        'industry': '行业动态',
        'paper': '论文研究',
        'tip': '技巧与观点'
    }
    return titles.get(api_cat, api_cat)

def cat_daily_label(api_cat):
    labels = {
        'ai-models': '模型发布',
        'ai-products': '产品更新',
        'industry': '行业动态',
        'paper': '论文',
        'tip': '技巧'
    }
    return labels.get(api_cat, '其他')

def generate_nf_items(items):
    """Generate nf-item HTML for index page."""
    result = []
    for item in items:
        api_cat = item.get('category', 'tip')
        dc = cat_mapping(api_cat)
        url = item.get('url', '#')
        title = html.escape(item.get('title', ''))
        time_str = fmt_time(item.get('publishedAt', ''))
        src = html.escape(clean_source(item.get('source', '')))
        
        result.append(
            f'    <a href="{url}" target="_blank" rel="noopener" class="nf-item" data-category="{dc}">\n'
            f'      <span class="nf-time">{time_str}</span>\n'
            f'      <span class="nf-title">{title}</span>\n'
            f'      <span class="nf-src">{src}</span>\n'
            f'    </a>'
        )
    return '\n'.join(result)

def generate_daily_content(items):
    """Generate daily page content (categories + items)."""
    # Group by category
    groups = {}
    for item in items:
        c = item.get('category', 'other')
        if c not in groups:
            groups[c] = []
        groups[c].append(item)
    
    order = ['ai-models', 'ai-products', 'industry', 'paper', 'tip']
    
    sections = []
    for cat in order:
        if cat not in groups or not groups[cat]:
            continue
        
        cat_items = groups[cat]
        icon = cat_daily_icon(cat)
        title = cat_daily_title(cat)
        
        parts = [f'<div class="daily-category">']
        parts.append(f'<h2>{icon} {title} <span class="cat-count">{len(cat_items)}</span></h2>')
        
        for item in cat_items:
            url = item.get('url', '#')
            title_text = html.escape(item.get('title', ''))
            pub_time = item.get('publishedAt', '')
            time_only = pub_time[11:16] if len(pub_time) >= 16 else ''
            src = html.escape(clean_source(item.get('source', '')))
            
            parts.append(
                f'<div class="daily-item">'
                f'<span class="daily-time">{time_only}</span>'
                f'<div class="daily-body">'
                f'<a href="{url}" target="_blank" rel="noopener" class="daily-title">{title_text}</a>'
                f'<span class="daily-src">{src}</span>'
                f'</div></div>'
            )
        
        parts.append('</div>')
        sections.append('\n'.join(parts))
    
    return '\n'.join(sections)

def main():
    items = load_api()
    
    # Count categories for stats
    counts = {'ai-models': 0, 'ai-products': 0, 'industry': 0, 'paper': 0, 'tip': 0}
    for item in items:
        c = item.get('category', '')
        if c in counts:
            counts[c] += 1
    
    # 1. Generate nf-items for index.html
    nf_html = generate_nf_items(items)
    
    # 2. Generate daily page content
    daily_content = generate_daily_content(items)
    
    # 3. Output to separate files
    with open('_nf_items.txt', 'w', encoding='utf-8') as f:
        f.write(nf_html)
    with open('_daily_content.txt', 'w', encoding='utf-8') as f:
        f.write(daily_content)
    with open('_stats.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(counts))
    
    print("Files written successfully")
    print(f"NF items count check: {len(items)}")
    for c, n in counts.items():
        print(f"  {c}: {n}")

if __name__ == '__main__':
    main()
