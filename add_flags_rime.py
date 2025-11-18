import os

for f in os.listdir("../../CARRA-evaluation/flags_rime"):
    st = f.replace(".csv", "")
    fr = f"../../CARRA-evaluation/flags_rime/{st}.csv"
    ff = f"flags/{st}.csv"

    if not os.path.exists(ff):
        continue

    # read rime flags (drop header)
    with open(fr, "r", encoding="utf-8") as src:
        rime_lines = src.read().splitlines()[1:]

    # read base file
    with open(ff, "r", encoding="utf-8") as base:
        existing = base.read().splitlines()

    # remove old rime lines
    existing = [
        ln for ln in existing
        if "automatically detected as rime-affected (bav)" not in ln
    ]

    # compute new lines to add
    new = [ln for ln in rime_lines if ln not in existing]

    # prepare final list
    final = existing.copy()

    if new:
        final.append("")
        final.extend(new)

    # collapse multiple blank lines
    cleaned = []
    last_empty = False
    for ln in final:
        if ln.strip() == "":
            if not last_empty:
                cleaned.append("")
            last_empty = True
        else:
            cleaned.append(ln)
            last_empty = False

    # write result
    with open(ff, "w", encoding="utf-8") as out:
        out.write("\n".join(cleaned) + "\n")
