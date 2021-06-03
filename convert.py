import os
import re
import json
import unicodedata

bracket_pattern = re.compile(r"\[.+?\]")


def convert_genre(category):
    return {
        "news": 0,
        "sports": 1,
        "information": 2,
        "drama": 3,
        "music": 4,
        "variety": 5,
        "cinema": 6,
        "anime": 7,
        "documentary": 8,
        "theater": 9,
        "hobby": 10,
        "welfare": 11,
        "etc": 12
    }[category]


def delete_brackets(content):
    return bracket_pattern.sub(content, "").strip()


if __name__ == "__main__":
    ID = 10000

    with open("recorded.json") as f:
        recorded = json.load(f)

    recorded_items = []
    video_file_items = []
    recorded_history_items = []
    for program in recorded:
        name = program["fullTitle"].strip()
        half_name = unicodedata.normalize("NFKC", name)
        description = (program.get("description", "") + "\nこの番組は Chinachu からインポートされました。").strip()
        extended = "\n".join([f"◇{x}\n{y}" for x, y in program["extra"].items()]) if "extra" in program else None
        recorded_items.append({
            "id": ID,
            "reserveId": None,
            "ruleId": None,
            "programId": int(program["id"], 36),
            "channelId": int(program["channel"]["id"], 36),
            "isProtected": False,
            "startAt": program["start"],
            "endAt": program["end"],
            "duration": program["seconds"] * 1000,
            "name": name,
            "halfWidthName": half_name,
            "description": description,
            "halfWidthDescription": unicodedata.normalize("NFKC", description),
            "extended": extended,
            "halfWidthExtended": unicodedata.normalize("NFKC", extended) if extended else None,

            "genre1": convert_genre(program["category"]),
            "subGenre1": 0,
            "genre2": None,
            "subGenre2": None,
            "genre3": None,
            "subGenre3": None,

            "videoType": "mpeg2",
            "videoResolution": "1080i",
            "videoStreamContent": 1,
            "videoComponentType": None,
            "audioSamplingRate": 48000,
            "audioComponentType": 3,

            "isRecording": False,
            "dropLogFileId": None
        })
        video_file_items.append({
            "size": os.path.getsize(program["recorded"]),
            "id": ID,
            "parentDirectoryName": os.path.basename(os.path.dirname(program["recorded"])),
            "filePath": os.path.basename(program["recorded"]),
            "type": "ts",
            "name": "TS",
            "recordedId": ID
        })
        recorded_history_items.append({
            "id": ID,
            "name": delete_brackets(half_name),
            "channelId": int(program["channel"]["id"], 36),
            "endAt": program["end"]
        })

        ID += 1

    with open("epgstation.json") as f:
        db = json.load(f)
        db["recordedItems"].extend(recorded_items)
        db["videoFileItems"].extend(video_file_items)
        db["recordedHistoryItems"].extend(recorded_history_items)

    with open("epgstation.new.json", "w") as f:
        json.dump(db, f, ensure_ascii=False)
