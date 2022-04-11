from typing import Optional, Sequence


RAW = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""


def most_common(seq: Sequence[str]) -> Optional[str]:
    ones = seq.count("1")
    zeros = seq.count("0")

    if ones == zeros:
        return None

    return "1" if ones > zeros else "0"


def least_common(seq: Sequence[str]) -> Optional[str]:
    index = most_common(seq) or "1"
    return ["1", "0"][int(index)]


def gamma_rate(raw_string: str) -> str:
    return "".join(most_common(column) for column in zip(*raw_string.split("\n")))


def eps_rate(raw_string: str) -> str:
    return "".join("0" if char == "1" else "1" for char in gamma_rate(raw_string))


def oxy_rate(raw_string: str) -> str:
    rows = raw_string.split("\n")
    pos = 0
    while len(rows) > 1:
        columns = list(zip(*rows))
        keep = most_common(columns[pos]) or "1"
        rows = [row for row in rows if row[pos] == keep]
        pos += 1

    return "".join(rows[0])


def co2_rate(raw_string: str) -> str:
    rows = raw_string.split("\n")
    pos = 0
    while len(rows) > 1:
        columns = list(zip(*rows))
        keep = least_common(columns[pos]) or "0"
        rows = [row for row in rows if row[pos] == keep]
        pos += 1

    return "".join(rows[0])


assert gamma_rate(RAW) == "10110"
assert eps_rate(RAW) == "01001"
assert oxy_rate(RAW) == "10111"
assert co2_rate(RAW) == "01010"


if __name__ == "__main__":
    with open("inputs/day_03.txt", encoding="utf-8") as f:
        raw = f.read()
    print(int(gamma_rate(raw), 2) * int(eps_rate(raw), 2))
    print(int(oxy_rate(raw), 2) * int(co2_rate(raw), 2))
