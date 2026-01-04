import json
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path("schedules")
OUT_DIR = Path(".")

today = datetime.now()
date_str = today.strftime("%Y-%m-%d")
date_compact = today.strftime("%Y%m%d")

DAY_NAMES = [
    "monday",    # 0
    "tuesday",   # 1
    "wednesday", # 2
    "thursday",  # 3
    "friday",    # 4
    "saturday",  # 5
    "sunday"     # 6
]

day_key = DAY_NAMES[today.weekday()]

def to_iso(base_date, time_str):
    if time_str == "24:00":
        d = base_date + timedelta(days=1)
        return d.strftime("%Y-%m-%dT00:00:00+09:00")
    return f"{base_date.strftime('%Y-%m-%d')}T{time_str}:00+09:00"

for ch_dir in BASE_DIR.iterdir():
    if not ch_dir.is_dir():
        continue

    schedule_file = ch_dir / f"{day_key}.json"
    if not schedule_file.exists():
        continue

    data = json.loads(schedule_file.read_text(encoding="utf-8"))
    channel = data["channel"]

    programs = []
    for start, end, title, desc in data["schedule"]:
        programs.append({
            "channel": channel,
            "title": title,
            "description": desc,
            "start": to_iso(today, start),
            "end": to_iso(today, end)
        })

    out_file = OUT_DIR / f"{channel}_{date_compact}.json"
    out_file.write_text(
        json.dumps(programs, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"generated: {out_file}")
