HEADER = "#### "
SEP = ":"
LINE_SEPARATE = "M5FdxitkkbomCWWFkhcHBstCu78ua7"


def search(ss: list[str], s: str) -> int:
    try:
        return ss.index(s)
    except ValueError:
        return -1


def parse_description(s: str) -> dict[str, str]:
    contents = s.split("\n")
    idx = search(contents, LINE_SEPARATE)
    ss = contents[idx + 1:]
    n = len(HEADER)
    lines = [l[n:] for l in ss if l[:n] == HEADER]
    ret: dict[str, str] = {}
    for line in lines:
        try:
            idx = line.index(SEP)
            key, val = line[:idx], line[idx+1:]
            ret[key] = val
        except ValueError:
            continue
    return ret


def dump_description(d: dict[str, str], orig_desc: str | None = None) -> str:
    orig = (
        orig_desc +
        "\n\n" +
        LINE_SEPARATE +
        "\n"
        if orig_desc is not None
        else ""
    )
    content = "\n".join([
        f"{HEADER}{k}{SEP}{v}"
        for k, v in d.items()
    ])
    return orig + content
