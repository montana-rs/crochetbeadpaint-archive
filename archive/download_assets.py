import json, urllib.request, time, os

manifest = json.load(open('download_manifest.json'))
ok, fail = 0, 0
for url, local_path in manifest:
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        ok += 1
        continue
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 archival-recovery'})
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read()
        with open(local_path, 'wb') as f:
            f.write(content)
        ok += 1
        print("OK", local_path)
    except Exception as e:
        print("FAIL", url, e)
        fail += 1
    time.sleep(1.5)

print(f"DONE OK={ok} FAIL={fail}")
