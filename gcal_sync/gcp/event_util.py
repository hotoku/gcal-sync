def parse_description(s: str) -> dict[str, str]:
    lines = [l[5:] for l in s.split() if l[:5] == "#### "]
    ret: dict[str, str] = {}
    for line in lines:
        try:
            idx = line.index(":")
            key, val = line[:idx], line[idx+1:]
            ret[key] = val
        except ValueError:
            continue
    return ret
