import os
import csv

output_file = "rime_detected_with_CARRA.csv"
rime_rows = []

for f in os.listdir("../../CARRA-evaluation/flags_rime"):
    if not f.endswith(".csv"):
        continue

    st = f.replace(".csv", "")
    ff = f"flags/{st}.csv"

    if not os.path.exists(ff):
        continue

    # Read original flag file
    with open(ff, "r", encoding="utf-8", newline="") as src:
        rows = list(csv.reader(src))

    if not rows:
        continue

    header = rows[0]
    kept_rows = [header]

    for row in rows[1:]:
        line = ",".join(row)

        # Extract only automatically detected RIME flags
        if (
            "RIME" in line
            or "automatically detected as rime-affected (bav)" in line
        ):
            rime_rows.append([st] + row)
        else:
            kept_rows.append(row)

    # Rewrite original file without the extracted RIME lines
    with open(ff, "w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out)
        writer.writerows(kept_rows)

# Save extracted flags
if rime_rows:
    with open(output_file, "w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["station"] + header)
        writer.writerows(rime_rows)
