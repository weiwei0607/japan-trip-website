import json

with open("decrypted_itinerary.js", "r") as f:
    data = json.loads(f.read())

for d in data:
    if d["day"] == "Day 1":
        for item in d["items"]:
            if item.get("name") == "海雲台海水浴場 釜山":
                item["time"] = "08:15"
                item["travel"] = "공항리무진1 機場巴士 金海→海雲台 約60-80分（07:10國內線航廈發→約08:15到）"
                
    if d["day"] == "Day 5":
        for item in d["items"]:
            if item.get("name") == "江島神社 江之島":
                item["time"] = "18:20"
                item["leaveTime"] = "19:20"
            if item.get("name") == "横濱港未來21 (夜景)":
                item["time"] = "20:20"
                
    if d["day"] == "Day 6":
        for item in d["items"]:
            if item.get("name") == "豐川稻荷 東京別院":
                item["time"] = "15:15"
                item["leaveTime"] = "15:40"
            elif item.get("name") == "日枝神社 東京":
                item["time"] = "15:50"
                item["leaveTime"] = "16:15"
            elif item.get("name") == "港区観光インフォメーションセンター":
                item["time"] = "16:35"
                item["leaveTime"] = "16:50"
            elif item.get("name") == "info＆cafe SQUARE 品川区荏原":
                item["time"] = "17:20"
                item["leaveTime"] = "17:35"
            elif item.get("name") == "澀谷站前空檔 (依體力自由切換選項) ☕🛍️":
                item["time"] = "18:05"

with open("decrypted_itinerary.js", "w") as f:
    json.dump(data, f, ensure_ascii=False)
