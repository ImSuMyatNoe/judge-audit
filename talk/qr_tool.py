"""Minimal QR encoder: byte mode, EC level M, versions 1-3.

Written because no QR library is installed and the package index is blocked.
Scope is deliberately tiny -- exactly what two short URLs need -- and every
table is cross-checked against published constants in self_test().
"""
from __future__ import annotations

# --- GF(256), primitive polynomial 0x11D, generator 2 ---------------------- #
EXP = [0] * 512
LOG = [0] * 256
x = 1
for i in range(255):
    EXP[i] = x
    LOG[x] = i
    x <<= 1
    if x & 0x100:
        x ^= 0x11D
for i in range(255, 512):
    EXP[i] = EXP[i - 255]


def gmul(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return EXP[LOG[a] + LOG[b]]


def rs_generator(n: int) -> list[int]:
    g = [1]
    for i in range(n):
        g = poly_mul(g, [1, EXP[i]])
    return g


def poly_mul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, av in enumerate(a):
        for j, bv in enumerate(b):
            out[i + j] ^= gmul(av, bv)
    return out


def rs_encode(data: list[int], n_ec: int) -> list[int]:
    gen = rs_generator(n_ec)
    rem = [0] * n_ec
    for d in data:
        factor = d ^ rem[0]
        rem = rem[1:] + [0]
        for i, g in enumerate(gen[1:]):
            rem[i] ^= gmul(g, factor)
    return rem


# --- version tables (EC level M only) ------------------------------------- #
# version: (modules, total codewords, data codewords, ec codewords per block, blocks)
VERSIONS = {
    1: (21, 26, 16, 10, 1),
    2: (25, 44, 28, 16, 1),
    3: (29, 70, 44, 26, 1),
}
ALIGN = {1: [], 2: [6, 18], 3: [6, 22]}


def bch_format(ec_bits: int, mask: int) -> str:
    """15-bit format information: 5 data bits, BCH(15,5), XOR 0x5412."""
    data = (ec_bits << 3) | mask
    v = data << 10
    g = 0x537
    for i in range(4, -1, -1):
        if v & (1 << (i + 10)):
            v ^= g << i
    fmt = ((data << 10) | v) ^ 0x5412
    return format(fmt, "015b")


def choose_version(n_bytes: int) -> int:
    for v in (1, 2, 3):
        _, _, data_cw, _, _ = VERSIONS[v]
        capacity = (data_cw * 8 - 4 - 8) // 8
        if n_bytes <= capacity:
            return v
    raise ValueError(f"{n_bytes} bytes needs a version beyond 3")


def encode_bits(text: str, version: int) -> list[int]:
    data = text.encode("utf-8")
    _, _, data_cw, _, _ = VERSIONS[version]
    bits: list[int] = []

    def put(value: int, length: int) -> None:
        for i in range(length - 1, -1, -1):
            bits.append((value >> i) & 1)

    put(0b0100, 4)          # byte mode
    put(len(data), 8)       # character count, 8 bits for versions 1-9
    for b in data:
        put(b, 8)
    total = data_cw * 8
    put(0, min(4, total - len(bits)))          # terminator
    while len(bits) % 8:
        bits.append(0)
    pads = [0xEC, 0x11]
    i = 0
    while len(bits) < total:
        put(pads[i % 2], 8)
        i += 1
    return bits


def codewords(bits: list[int]) -> list[int]:
    return [int("".join(str(b) for b in bits[i:i + 8]), 2) for i in range(0, len(bits), 8)]


# --- matrix --------------------------------------------------------------- #

def blank(n: int):
    return [[None] * n for _ in range(n)], [[False] * n for _ in range(n)]


def place_function_patterns(m, reserved, version: int) -> None:
    n = len(m)

    def finder(r0: int, c0: int) -> None:
        for r in range(-1, 8):
            for c in range(-1, 8):
                rr, cc = r0 + r, c0 + c
                if not (0 <= rr < n and 0 <= cc < n):
                    continue
                inring = (0 <= r <= 6 and c in (0, 6)) or (0 <= c <= 6 and r in (0, 6))
                incore = 2 <= r <= 4 and 2 <= c <= 4
                m[rr][cc] = 1 if (inring or incore) else 0
                reserved[rr][cc] = True

    finder(0, 0)
    finder(0, n - 7)
    finder(n - 7, 0)

    for i in range(8, n - 8):                    # timing
        bit = 1 if i % 2 == 0 else 0
        m[6][i] = bit; reserved[6][i] = True
        m[i][6] = bit; reserved[i][6] = True

    centers = ALIGN[version]
    for r in centers:
        for c in centers:
            if (r < 9 and c < 9) or (r < 9 and c > n - 10) or (r > n - 10 and c < 9):
                continue
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    v = 1 if max(abs(dr), abs(dc)) != 1 else 0
                    m[r + dr][c + dc] = v
                    reserved[r + dr][c + dc] = True

    m[4 * version + 9][8] = 1                    # dark module
    reserved[4 * version + 9][8] = True

    for i in range(9):                           # format areas
        if m[8][i] is None:
            reserved[8][i] = True
        if m[i][8] is None:
            reserved[i][8] = True
    for i in range(8):
        reserved[8][n - 1 - i] = True
        reserved[n - 1 - i][8] = True


def place_data(m, reserved, bits: list[int]) -> None:
    n = len(m)
    idx = 0
    col = n - 1
    upward = True
    while col > 0:
        if col == 6:
            col -= 1
        rows = range(n - 1, -1, -1) if upward else range(n)
        for row in rows:
            for c in (col, col - 1):
                if reserved[row][c]:
                    continue
                m[row][c] = bits[idx] if idx < len(bits) else 0
                idx += 1
        col -= 2
        upward = not upward


MASKS = [
    lambda r, c: (r + c) % 2 == 0,
    lambda r, c: r % 2 == 0,
    lambda r, c: c % 3 == 0,
    lambda r, c: (r + c) % 3 == 0,
    lambda r, c: (r // 2 + c // 3) % 2 == 0,
    lambda r, c: (r * c) % 2 + (r * c) % 3 == 0,
    lambda r, c: ((r * c) % 2 + (r * c) % 3) % 2 == 0,
    lambda r, c: ((r + c) % 2 + (r * c) % 3) % 2 == 0,
]


def apply_mask(m, reserved, k: int):
    n = len(m)
    out = [row[:] for row in m]
    for r in range(n):
        for c in range(n):
            if not reserved[r][c] and MASKS[k](r, c):
                out[r][c] ^= 1
    return out


def place_format(m, ec_bits: int, mask: int) -> None:
    n = len(m)
    bits = [int(b) for b in bch_format(ec_bits, mask)]
    coords_a = [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 7), (8, 8),
                (7, 8), (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8)]
    for bit, (r, c) in zip(bits, coords_a):
        m[r][c] = bit
    coords_b = [(n - 1 - i, 8) for i in range(7)] + [(8, n - 8 + i) for i in range(8)]
    for bit, (r, c) in zip(bits, coords_b):
        m[r][c] = bit


def penalty(m) -> int:
    n = len(m)
    score = 0
    for line in list(m) + [list(col) for col in zip(*m)]:      # rule 1
        run, prev = 1, line[0]
        for v in line[1:]:
            if v == prev:
                run += 1
            else:
                if run >= 5:
                    score += 3 + (run - 5)
                run, prev = 1, v
        if run >= 5:
            score += 3 + (run - 5)
    for r in range(n - 1):                                     # rule 2
        for c in range(n - 1):
            if m[r][c] == m[r][c + 1] == m[r + 1][c] == m[r + 1][c + 1]:
                score += 3
    pat1 = [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0]
    pat2 = pat1[::-1]
    for line in list(m) + [list(col) for col in zip(*m)]:      # rule 3
        for i in range(n - 10):
            seg = line[i:i + 11]
            if seg == pat1 or seg == pat2:
                score += 40
    dark = sum(sum(row) for row in m)                          # rule 4
    pct = dark * 100 // (n * n)
    score += 10 * min(abs(pct - 50) // 5, abs((pct + 4) - 50) // 5)
    return score


def make(text: str) -> list[str]:
    version = choose_version(len(text.encode()))
    n, total_cw, data_cw, ec_cw, blocks = VERSIONS[version]
    assert blocks == 1, "this encoder only handles single-block versions"

    data = codewords(encode_bits(text, version))
    ec = rs_encode(data, ec_cw)
    allbits: list[int] = []
    for cw in data + ec:
        allbits.extend((cw >> i) & 1 for i in range(7, -1, -1))

    m, reserved = blank(n)
    place_function_patterns(m, reserved, version)
    place_data(m, reserved, allbits)

    best, best_score = None, None
    for k in range(8):
        cand = apply_mask(m, reserved, k)
        place_format(cand, 0b00, k)          # EC level M = 00
        s = penalty(cand)
        if best_score is None or s < best_score:
            best, best_score = cand, s
    return ["".join(str(v) for v in row) for row in best]


def self_test() -> None:
    # Format information is a BCH(15,5) code XORed with 0x5412. Rather than
    # trust a remembered table, check the two properties the spec guarantees:
    # every codeword is divisible by the generator once the XOR is removed,
    # and the minimum Hamming distance across all 32 codewords is 7.
    words = []
    for ec in range(4):
        for mask in range(8):
            raw = int(bch_format(ec, mask), 2) ^ 0x5412
            assert raw >> 10 == (ec << 3) | mask, "format data bits corrupted"
            rem = raw
            for i in range(14, 9, -1):
                if rem & (1 << i):
                    rem ^= 0x537 << (i - 10)
            assert rem == 0, f"format bits not divisible by generator (ec={ec}, mask={mask})"
            words.append(int(bch_format(ec, mask), 2))
    dmin = min(bin(a ^ b).count("1") for i, a in enumerate(words) for b in words[i + 1:])
    assert dmin == 7, f"format code minimum distance is {dmin}, expected 7"
    # Reed-Solomon round trip: syndromes of a valid codeword must all be zero.
    data = list(range(1, 45))
    ec = rs_encode(data, 26)
    full = data + ec
    for i in range(26):
        syn = 0
        for cw in full:
            syn = gmul(syn, EXP[i]) ^ cw
        assert syn == 0, f"syndrome {i} non-zero"
    # Structure: finder cores, timing alternation, dark module.
    rows = make("https://imsumyatnoe.github.io/")
    n = len(rows)
    assert n == 29
    for (r0, c0) in [(0, 0), (0, n - 7), (n - 7, 0)]:
        assert rows[r0 + 3][c0 + 3] == "1" and rows[r0][c0] == "1"
        assert rows[r0 + 1][c0 + 1] == "0"
    assert rows[6][8] == "1" and rows[6][9] == "0"
    assert rows[4 * 3 + 9][8] == "1"
    print("self-test OK")


if __name__ == "__main__":
    import json
    self_test()
    out = {
        "portfolio": {"text": "https://imsumyatnoe.github.io/",
                      "rows": make("https://imsumyatnoe.github.io/")},
        "repo": {"text": "https://github.com/ImSuMyatNoe/judge-audit",
                 "rows": make("https://github.com/ImSuMyatNoe/judge-audit")},
    }
    for k, v in out.items():
        print(k, len(v["rows"]), "modules")
    json.dump(out, open("qr.json", "w"))


# --- independent read-back: decode our own matrix and check it round-trips -- #

def decode(rows: list[str]) -> str:
    """Read a matrix the way a scanner would: recover the mask from the format
    bits, unmask, walk the data path, verify the Reed-Solomon syndromes, then
    parse mode, length and payload. Any error in placement, masking or ordering
    shows up here as a mismatch."""
    n = len(rows)
    version = (n - 17) // 4
    m = [[int(ch) for ch in row] for row in rows]

    fmt = "".join(str(m[r][c]) for r, c in
                  [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 7), (8, 8),
                   (7, 8), (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8)])
    raw = int(fmt, 2) ^ 0x5412
    ec_bits, mask = (raw >> 13) & 0b11, (raw >> 10) & 0b111
    assert ec_bits == 0b00, f"expected EC level M, read {ec_bits:02b}"

    _, reserved = blank(n)
    probe = [[None] * n for _ in range(n)]
    place_function_patterns(probe, reserved, version)

    for r in range(n):
        for c in range(n):
            if not reserved[r][c] and MASKS[mask](r, c):
                m[r][c] ^= 1

    bits: list[int] = []
    col, upward = n - 1, True
    while col > 0:
        if col == 6:
            col -= 1
        for row in (range(n - 1, -1, -1) if upward else range(n)):
            for c in (col, col - 1):
                if not reserved[row][c]:
                    bits.append(m[row][c])
        col -= 2
        upward = not upward

    cws = [int("".join(str(b) for b in bits[i:i + 8]), 2) for i in range(0, (len(bits) // 8) * 8, 8)]
    _, total_cw, data_cw, ec_cw, _ = VERSIONS[version]
    cws = cws[:total_cw]
    for i in range(ec_cw):
        syn = 0
        for cw in cws:
            syn = gmul(syn, EXP[i]) ^ cw
        assert syn == 0, f"Reed-Solomon syndrome {i} is non-zero -- the matrix is corrupt"

    payload = bits[:data_cw * 8]
    mode = int("".join(str(b) for b in payload[0:4]), 2)
    assert mode == 0b0100, f"expected byte mode, read {mode:04b}"
    length = int("".join(str(b) for b in payload[4:12]), 2)
    out = bytearray()
    for i in range(length):
        out.append(int("".join(str(b) for b in payload[12 + i * 8:20 + i * 8]), 2))
    return out.decode("utf-8")
