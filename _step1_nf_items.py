#!/usr/bin/env python3
"""Step 1: Generate nf-items HTML from aihot_selected.json"""
import json
from datetime import datetime, timezone, timedelta

BJT = timezone(timedelta(hours=8))
TODAY = datetime.now(BJT).strftime('%Y-%m-%d')
TODAY_DT = datetime.now(BJT)

CAT_MAP = {
    'ai-models': 'ai-models',
    'ai-products': 'ai-products', 
    'industry': 'industry',
    'paper': 'paper',
    'tip': 'tip'
}

def format_time(published_at):
    """Convert UTC time to BJT (UTC+8)"""
    if not published_at:
        return ''
    try:
        utc_dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
        bjt_dt = utc_dt.astimezone(BJT)
        now = datetime.now(BJT)
        today_str = now.strftime('%Y-%m-%d')
        
        if bjt_dt.strftime('%Y-%m-%d') == today_str:
            return f"今天 {bjt_dt.strftime('%H:%M')}"
        elif (now - bjt_dt).days == 1 and now.strftime('%Y-%m-%d') != bjt_dt.strftime('%Y-%m-%d'):
            return f"昨天 {bjt_dt.strftime('%H:%M')}"
        elif (now - bjt_dt).days <= 1 and (now - bjt_dt).days >= 0:
            # Same day or yesterday (cross midnight check)
            diff_days = (now.date() - bjt_dt.date()).days
            if diff_days == 0:
                return f"今天 {bjt_dt.strftime('%H:%M')}"
            elif diff_days == 1:
                return f"昨天 {bjt_dt.strftime('%H:%M')}"
            else:
                return bjt_dt.strftime('%m/%d %H:%M')
        else:
            return bjt_dt.strftime('%m/%d %H:%M')
    except:
        return published_at[:16] if len(published_at) >= 16 else published_at

def clean_source(source):
    """Clean source name"""
    if not source:
        return ''
    # Remove X： prefix
    import re
    s = re.sub(r'^X[：:]', '', source)
    # Remove parenthetical comments like (@shao__meng), （RSS）, etc.
    s = re.sub(r'[（(][^)）]*[)）]', '', s)
    s = s.strip()
    # Truncate to 18 chars
    if len(s) > 18:
        s = s[:15] + '...'
    return s

data = json.load(open('aihot_selected.json', encoding='utf-8'))
items = data['items']

lines = []
for item in items:
    cat = item.get('category', 'tip')
    cat_attr = CAT_MAP.get(cat, 'tip')
    title = item.get('title', '')
    url = item.get('url', '#')
    time_str = format_time(item.get('publishedAt', ''))
    source = clean_source(item.get('source', ''))
    
    # Escape quotes in title for HTML attribute safety
    title_escaped = title.replace('"', '&quot;').replace("'", '&#39;')
    
    line = f'      <a href="{url}" target="_blank" rel="noopener" class="nf-item" data-category="{cat_attr}">\n'
    line += f'        <span class="nf-time">{time_str}</span>\n'
    line += f'        <span class="nf-title">{title_escaped}</span>\n'
    line += f'        <span class="nf-src">{source}</span>\n'
    line += f'      </a>'
    lines.append(line)

output = '\n'.join(lines)
with open('_nf_items_output.txt', 'w', encoding='utf-8') as f:
    f.write(output)

print(f"✅ Generated {len(lines)} nf-items")
