import json
import sys
import time
import requests
sys.path.insert(0, '/Users/daibao')
from notion_config import TOKEN

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

PAGE_IDS = {
    "Day 1": "36541fbb-b7a8-8134-9f8c-e39f483457c3",
    "Day 2": "36541fbb-b7a8-8171-9365-f306784828c0",
    "Day 3": "37441fbb-b7a8-81bb-b3be-c4c2fd2d06fe",
    "Day 4": "36541fbb-b7a8-8186-aa2d-e8f1ee9b9a34",
    "Day 5": "36541fbb-b7a8-814a-97e9-fbbd762d4965",
    "Day 6": "36541fbb-b7a8-819c-99a5-eac01246a932",
    "Day 7": "36541fbb-b7a8-81c3-83fa-c1b16096b601",
    "Day 8": "36541fbb-b7a8-81b8-9abc-c083bfc4c313",
    "Day 9": "36541fbb-b7a8-81d8-925e-cdaab8c989e5",
    "Day 10": "36541fbb-b7a8-8124-84c7-cb0ba4533868",
    "Day 11": "37441fbb-b7a8-8147-a05d-dc2e7e885057",
}

def api_get(url):
    r = requests.get(url, headers=HEADERS, timeout=60)
    time.sleep(0.35)
    return r

def api_delete(url):
    r = requests.delete(url, headers=HEADERS, timeout=60)
    time.sleep(0.35)
    return r

def api_patch(url, data):
    r = requests.patch(url, headers=HEADERS, json=data, timeout=60)
    time.sleep(0.35)
    return r

def rich(text):
    return [{"type": "text", "text": {"content": text}}]

def make_block(text, block_type="bulleted_list_item"):
    if block_type == "heading_2":
        return {"object": "block", "type": "heading_2", "heading_2": {"rich_text": rich(text)}}
    if block_type == "divider":
        return {"object": "block", "type": "divider", "divider": {}}
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": rich(text)}}

def strip_html(text):
    if not text:
        return ""
    # 移除 HTML 標籤
    text = text.replace("<br>", " ").replace("<br/>", " ").replace("<br />", " ")
    text = text.replace("<b>", "").replace("</b>", "")
    text = text.replace("<s>", "").replace("</s>", "")
    text = text.replace("<span ", "").replace("</span>", "")
    # 簡易移除其他標籤屬性
    text = text.replace('style="color:#e53e3e;font-weight:bold;"', "")
    text = text.replace('style="color:#16a34a;font-weight:bold;"', "")
    text = text.replace('style="color:#2b6cb0;font-weight:bold;"', "")
    text = text.replace('style="color:#c05621;font-weight:bold;"', "")
    text = text.replace('style="color:red;font-weight:bold;"', "")
    text = text.replace('style="font-size:0.85em; color:#6b7280; font-weight:normal;"', "")
    import re
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def sync_day(day):
    page_id = PAGE_IDS.get(day['day'])
    if not page_id:
        print(f"SKIP {day['day']}: no page ID")
        return
    
    print(f"\nSyncing {day['day']} ({page_id})...")
    
    # 1. 取得現有 blocks
    r = api_get(f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100")
    if r.status_code != 200:
        print(f"  Failed to fetch children: {r.status_code} {r.text[:200]}")
        return
    blocks = r.json().get('results', [])
    print(f"  Found {len(blocks)} existing blocks")
    
    # 2. 只刪除 bulleted_list_item 類型的 blocks（行程列表）
    deleted = 0
    for b in blocks:
        if b.get('type') != 'bulleted_list_item':
            continue
        bid = b['id']
        dr = api_delete(f"https://api.notion.com/v1/blocks/{bid}")
        if dr.status_code in [200, 204]:
            deleted += 1
        else:
            print(f"  DELETE failed {bid}: {dr.status_code}")
    print(f"  Deleted {deleted} bulleted_list_item blocks")
    
    # 3. 建立新 blocks
    new_children = []
    new_children.append(make_block(f"{day['day']}｜{day['date']}", "heading_2"))
    if day.get('hotel'):
        new_children.append(make_block(f"🏨 住宿: {day['hotel']}"))
    if day.get('note'):
        note = strip_html(day['note'])
        if note:
            new_children.append(make_block(f"💡 {note}"))
    new_children.append(make_block("", "divider"))
    
    for item in day['items']:
        time_str = item.get('time', '')
        name = item.get('name', '')
        cat = item.get('category', '')
        note = strip_html(item.get('note', ''))
        travel = strip_html(item.get('travel', ''))
        leave = item.get('leaveTime', '')
        
        line = f"{time_str} {name}"
        if travel:
            line += f" （{travel}）"
        if leave:
            line += f" → {leave}"
        if note:
            line += f" / {note[:120]}"
        new_children.append(make_block(line))
    
    # Notion 一次最多 append 100 個 children
    for i in range(0, len(new_children), 90):
        chunk = new_children[i:i+90]
        pr = api_patch(f"https://api.notion.com/v1/blocks/{page_id}/children", {"children": chunk})
        if pr.status_code != 200:
            print(f"  PATCH failed: {pr.status_code} {pr.text[:300]}")
            return
        print(f"  Appended {len(chunk)} blocks")
    
    print(f"  ✅ {day['day']} sync complete")

if __name__ == "__main__":
    with open('decrypted_itinerary_latest.json', 'r', encoding='utf-8') as f:
        days = json.load(f)
    
    for day in days:
        sync_day(day)
    
    print("\n🎉 All days synced to Notion!")
