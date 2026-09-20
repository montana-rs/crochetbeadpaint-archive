import json, urllib.request, time, os

manifest = json.load(open('download_manifest.json'))
retried, ok, fail = 0, 0, 0
for url, local_path in manifest:
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        continue
    retried += 1
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 archival-recovery'})
            with urllib.request.urlopen(req, timeout=25) as resp:
                content = resp.read()
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                f.write(content)
            ok += 1
            print("OK", local_path)
            break
        except Exception as e:
            print(f"attempt {attempt} FAIL", url, e)
            time.sleep(5)
    else:
        fail += 1
    time.sleep(2)

print(f"DONE retried={retried} ok={ok} fail={fail}")
