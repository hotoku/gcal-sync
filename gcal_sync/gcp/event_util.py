HEADER = "#### "
SEP = ":"


def parse_description(s: str) -> dict[str, str]:
    n = len(HEADER)
    lines = [l[n:] for l in s.split("\n") if l[:n] == HEADER]
    ret: dict[str, str] = {}
    for line in lines:
        try:
            idx = line.index(SEP)
            key, val = line[:idx], line[idx+1:]
            ret[key] = val
        except ValueError:
            continue
    return ret


def dump_description(d: dict[str, str]) -> str:
    return "\n".join([
        f"{HEADER}{k}{SEP}{v}"
        for k, v in d.items()
    ])
