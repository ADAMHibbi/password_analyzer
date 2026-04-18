#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║     ADVANCED PASSWORD PATTERN GENERATOR & ANALYZER v2.0         ║
║     [ Educational & Password Strength Awareness Tool ]           ║
╚══════════════════════════════════════════════════════════════════╝

DISCLAIMER: This tool is for educational and password strength
awareness purposes only. Use it to understand how predictable
password patterns are, and to create STRONGER, more secure passwords.
"""

import random
import sys
import os

# ─── ANSI Color Codes ────────────────────────────────────────────────────────────
G  = "\033[92m"   # green
C  = "\033[96m"   # cyan
Y  = "\033[93m"   # yellow
R  = "\033[91m"   # red
DM = "\033[90m"   # dark/gray
W  = "\033[97m"   # white
RS = "\033[0m"    # reset

# ─── Banner & UI Helpers ─────────────────────────────────────────────────────────

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def print_banner():
    print(f"""{G}
  ██████╗  █████╗ ███████╗███████╗██╗    ██╗██████╗
  ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔══██╗
  ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║  ██║
  ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║  ██║
  ██║     ██║  ██║███████║███████║╚███╔███╔╝██████╔╝
  ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝╚═════╝
{RS}{C}         A N A L Y Z E R   &   G E N E R A T O R  ──  v2.0{RS}
{DM}  ─────────────────────────────────────────────────────────────
  [ Educational ]  [ Awareness Tool ]  [ 8-9 Char Patterns Only ]
  ─────────────────────────────────────────────────────────────{RS}
""")

def print_disclaimer():
    print(f"""{Y}
  ┌─────────────────────────────────────────────────────────────┐
  │  ⚠  DISCLAIMER                                              │
  │  This tool is for educational and password strength         │
  │  awareness purposes only. It shows how predictable common   │
  │  password patterns are — use this insight to build STRONGER │
  │  and truly random passwords for yourself.                   │
  └─────────────────────────────────────────────────────────────┘{RS}
""")

def section(title):
    bar = "─" * (54 - len(title))
    print(f"\n{C}  ╔══ {title} {bar}{RS}")

def prompt(label, required=False):
    tag = f"{R}[REQUIRED]{RS}" if required else f"{DM}[optional]{RS}"
    return input(f"  {G}▶{RS}  {label} {tag}: ").strip()

def info(msg):  print(f"  {C}ℹ{RS}  {msg}")
def warn(msg):  print(f"  {Y}⚠{RS}  {msg}")
def ok(msg):    print(f"  {G}✔{RS}  {msg}")
def err(msg):   print(f"  {R}✗{RS}  {msg}")

# ─── Input Collection ────────────────────────────────────────────────────────────

def collect_inputs():
    """Prompt user for all required and optional inputs."""
    section("TARGET INPUT DATA")
    print(f"{DM}  Fill in the fields below. Press Enter to skip optional fields.{RS}\n")

    while True:
        first = prompt("First Name", required=True)
        if first: break
        err("First name cannot be empty.")

    while True:
        last = prompt("Last Name", required=True)
        if last: break
        err("Last name cannot be empty.")

    birth_raw = prompt("Birth Date (YYYY or YYYYMMDD)")
    nickname  = prompt("Nickname")
    kw_raw    = prompt("Keywords (comma-separated, max 5)")

    keywords = [k.strip() for k in kw_raw.split(",") if k.strip()][:5] if kw_raw else []

    # Parse birth date
    birth_year = birth_short = birth_digits = ""
    if birth_raw:
        d = birth_raw.replace("-", "").replace("/", "")
        if d.isdigit():
            if len(d) == 4:
                birth_year = d; birth_short = d[2:]; birth_digits = d
            elif len(d) == 8:
                birth_year = d[:4]; birth_short = d[2:4]; birth_digits = d
        if not birth_year:
            warn("Birth date format not recognized — skipping.")

    return {
        "first":        first.lower(),
        "last":         last.lower(),
        "first_cap":    first.capitalize(),
        "last_cap":     last.capitalize(),
        "first_up":     first.upper(),
        "last_up":      last.upper(),
        "nickname":     nickname.lower() if nickname else "",
        "nick_cap":     nickname.capitalize() if nickname else "",
        "birth_year":   birth_year,
        "birth_short":  birth_short,
        "birth_digits": birth_digits,
        "keywords":     [k.lower() for k in keywords],
    }

# ─── Pattern Engine ──────────────────────────────────────────────────────────────

LEET = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7", "l": "1"}

SUFFIXES = [
    "123", "1234", "12345", "321", "0", "1", "2", "00", "01", "99",
    "!", "@", "#", "!!", "123!", "2024", "2025", "2023", "2022",
    "007", "777", "000", "111", "666", "786", "101", "_1", "_123",
    "@123", "!1", "#1", "1!", "0!", "1@", "22", "33", "44", "55",
    "88", "10", "11", "12", "13", "21", "23", "456", "789", "000",
    "002", "003", "911", "100", "200", "007!", "1234!", "123#",
]

PREFIXES = ["@", "!", "#", "mr", "ms", "dr", "my", "the", "0", "1"]

SPECIAL = ["!", "@", "#", "$", "*", ".", "_", "-"]


def leet(word):
    """Convert word to leet-speak."""
    return "".join(LEET.get(c, c) for c in word.lower())


def variants(word):
    """Return capitalization and leet variants of a word."""
    if not word:
        return []
    return list({
        word.lower(),
        word.capitalize(),
        word.upper(),
        leet(word),
        leet(word).capitalize(),
        word[0].upper() + word[1:].lower(),
    })


def enforce_length(candidates, lo=8, hi=9):
    """Filter passwords to only those with length in [lo, hi]."""
    return {p for p in candidates if lo <= len(p) <= hi}


def pad_or_trim(base, target_lengths=(8, 9)):
    """
    Given a base string, yield versions padded with digits
    or trimmed to fit exactly into target_lengths.
    """
    results = set()
    b = base
    for tl in target_lengths:
        diff = tl - len(b)
        if diff == 0:
            results.add(b)
        elif diff > 0:
            # Pad with common digit suffixes
            for suf in ["1", "12", "123", "0", "01", "00", "99", "21", "!", "@"]:
                candidate = b + suf
                if len(candidate) == tl:
                    results.add(candidate)
                elif len(candidate) < tl:
                    # further pad
                    for extra in ["1", "2", "3", "!", "@", "0"]:
                        c2 = candidate + extra
                        if len(c2) == tl:
                            results.add(c2)
        else:
            # Trim — keep first tl chars (only if makes sense)
            trimmed = b[:tl]
            results.add(trimmed)
    return results


def build_raw_candidates(data):
    """Generate a large pool of raw password patterns before length filtering."""
    raw = set()

    f     = data["first"]
    l     = data["last"]
    fc    = data["first_cap"]
    lc    = data["last_cap"]
    fu    = data["first_up"]
    lu    = data["last_up"]
    nick  = data["nickname"]
    nc    = data["nick_cap"]
    year  = data["birth_year"]
    ys    = data["birth_short"]
    bdig  = data["birth_digits"]
    kws   = data["keywords"]

    # ── Helpers ──────────────────────────────────────────────────
    def add_with_suffixes(base):
        for suf in SUFFIXES:
            raw.add(base + suf)

    def add_with_specials(base):
        for sp in SPECIAL:
            raw.add(base + sp)
            raw.add(sp + base)

    # ── Name variants ────────────────────────────────────────────
    for v in variants(f) + variants(l):
        add_with_suffixes(v)
        add_with_specials(v)
        raw.add(v)

    # ── First+Last combos ────────────────────────────────────────
    combos = [
        f + l, l + f,
        fc + l, f + lc, fc + lc, fu + l, f + lu,
        f[0] + l, f + l[0], fc + l[0], f[0] + lc,
        f + "." + l, l + "." + f,
        f + "_" + l, l + "_" + f,
        f + "-" + l, l + "-" + f,
        f + "@" + l, l + "@" + f,
        f[:3] + l, f + l[:3], f[:4] + l[:4],
        fc[:3] + lc, fc + lc[:3],
    ]
    for combo in combos:
        raw.add(combo)
        add_with_suffixes(combo)

    # ── Birth year patterns ──────────────────────────────────────
    if year:
        for v in variants(f) + variants(l):
            raw.add(v + year)
            raw.add(v + ys)
            raw.add(year + v)
            raw.add(ys + v)
        raw.add(f + l + year)
        raw.add(fc + lc + ys)
        raw.add(year + f)
        raw.add(year + l)
        raw.add(f[:4] + year)
        raw.add(l[:4] + year)
        if bdig and len(bdig) == 8:
            raw.add(f + bdig[:4])
            raw.add(l + bdig[:4])
            raw.add(f[:4] + bdig[:4])
            raw.add(l[:4] + bdig[:4])
            raw.add(bdig[:4] + f[:4])
            raw.add(bdig[4:] + f[:3])

    # ── Nickname patterns ────────────────────────────────────────
    if nick:
        for v in variants(nick):
            raw.add(v)
            add_with_suffixes(v)
        if year:
            raw.add(nick + year)
            raw.add(nc + year)
            raw.add(nick + ys)
        raw.add(nick + f)
        raw.add(nick + l)
        raw.add(f + nick)
        raw.add(l + nick)
        raw.add(leet(nick) + "123")
        raw.add(leet(nick) + year if year else leet(nick) + "1")
        for suf in SUFFIXES:
            raw.add(nick + suf)

    # ── Keyword patterns ─────────────────────────────────────────
    for kw in kws:
        for v in variants(kw):
            raw.add(v)
            add_with_suffixes(v)
        raw.add(kw + f)
        raw.add(kw + l)
        raw.add(f + kw)
        raw.add(l + kw)
        if year:
            raw.add(kw + year)
            raw.add(kw + ys)
        raw.add(leet(kw) + "123")
        for sp in SPECIAL:
            raw.add(kw + sp + "1")

    # ── Prefix patterns ──────────────────────────────────────────
    for pfx in PREFIXES:
        for name in [f, l, fc, lc, nick, nc]:
            if name:
                raw.add(pfx + name)
                raw.add(name + pfx)

    # ── Number-heavy combos ───────────────────────────────────────
    years_extra = ["2020", "2021", "2022", "2023", "2024", "2025", "1999", "1998"]
    for yr in years_extra:
        raw.add(f[:4] + yr)
        raw.add(l[:4] + yr)
        raw.add(yr[:2] + f[:3] + yr[2:])

    # ── Leet combos ───────────────────────────────────────────────
    raw.add(leet(f + l))
    raw.add(leet(l + f))
    if nick:
        raw.add(leet(nick + f))
        raw.add(leet(f + nick))

    return raw


def generate_passwords(data, target=1000):
    """
    Build raw candidates, filter to 8-9 char length, pad/trim
    others to reach `target` count, then return shuffled list.
    """
    raw = build_raw_candidates(data)

    # First pass: strict 8-9 filter
    valid = enforce_length(raw)

    # Second pass: pad/trim out-of-range strings to fill the pool
    if len(valid) < target:
        extras = set()
        for cand in raw:
            if len(cand) < 8 or len(cand) > 9:
                extras.update(pad_or_trim(cand, (8, 9)))
        valid.update(extras)

    # Third pass: pad base names with sequential numbers to reach target
    if len(valid) < target:
        bases = [data["first"], data["last"], data["first_cap"], data["last_cap"]]
        if data["nickname"]:
            bases.append(data["nickname"])
        bases += [k for k in data["keywords"]]
        i = 0
        while len(valid) < target * 2 and i < 100000:
            for b in bases:
                for tl in (8, 9):
                    diff = tl - len(b)
                    if diff > 0:
                        suffix = str(i).zfill(diff)
                        if len(suffix) == diff:
                            valid.add(b + suffix)
            i += 1

    # Final dedup + length check
    final = list(enforce_length(valid))
    random.shuffle(final)
    return final[:target]

# ─── Similarity Engine ───────────────────────────────────────────────────────────

def levenshtein(s1, s2):
    """Compute Levenshtein (edit) distance between two strings."""
    m, n = len(s1), len(s2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[:]
        dp[0] = i
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[j] = prev[j-1]
            else:
                dp[j] = 1 + min(prev[j-1], prev[j], dp[j-1])
    return dp[n]


def similarity_score(pw1, pw2):
    """
    Return a 0–100 similarity score between two passwords.
    Combines Levenshtein distance and positional character matching.
    """
    max_len = max(len(pw1), len(pw2), 1)
    lev = levenshtein(pw1, pw2)
    lev_score = max(0, 100 - int((lev / max_len) * 100))

    # Positional match bonus
    pos_matches = sum(1 for a, b in zip(pw1, pw2) if a == b)
    pos_score = int((pos_matches / max_len) * 100)

    return round((lev_score * 0.7) + (pos_score * 0.3))


def find_top_similar(target_pw, passwords, top_n=10):
    """Return top N most similar passwords with scores."""
    scored = [(pw, similarity_score(target_pw, pw)) for pw in passwords]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]

# ─── Analysis Module ─────────────────────────────────────────────────────────────

def analyze_password(passwords):
    """
    Prompt user for their password and analyze it against
    the generated list for exact match and similarity.
    """
    section("PASSWORD ANALYSIS")
    print(f"{DM}  Enter your password to test how predictable it might be.{RS}")
    print(f"{DM}  This input is NOT stored or transmitted anywhere.{RS}\n")
    user_pw = input(f"  {G}▶{RS}  Your password {DM}[press Enter to skip]{RS}: ").strip()

    if not user_pw:
        info("Analysis skipped.")
        return None

    results = {"password": user_pw, "found": False, "top10": []}

    print(f"\n  {DM}Scanning {len(passwords)} patterns...{RS}")

    # Exact match check
    pw_set = set(passwords)
    if user_pw in pw_set:
        results["found"] = True
        print(f"\n  {R}┌──────────────────────────────────────────────────────────┐{RS}")
        print(f"  {R}│  ⚠  EXACT MATCH FOUND in generated patterns!              │{RS}")
        print(f"  {R}│  Your password '{user_pw}' is highly predictable.         │{RS}")
        print(f"  {R}│  Change it IMMEDIATELY to something random and unique.    │{RS}")
        print(f"  {R}└──────────────────────────────────────────────────────────┘{RS}")
    else:
        print(f"\n  {G}✔{RS}  Exact password NOT found in generated list.")
        print(f"  {DM}  (This does not mean it's safe — checking similarity...){RS}")

    # Similarity top 10
    top10 = find_top_similar(user_pw, passwords, top_n=10)
    results["top10"] = top10

    section("TOP 10 SIMILAR PATTERNS")
    print(f"\n  {'#':<4} {'Password':<14} {'Score':>6}  {'Bar'}")
    print(f"  {DM}{'─'*50}{RS}")
    for rank, (pw, score) in enumerate(top10, 1):
        bar_len = score // 10
        bar = f"{G}{'█' * bar_len}{DM}{'░' * (10 - bar_len)}{RS}"
        flag = f" {R}← HIGH RISK{RS}" if score >= 80 else (f" {Y}← WATCH OUT{RS}" if score >= 60 else "")
        print(f"  {rank:<4} {C}{pw:<14}{RS} {score:>5}%  {bar}{flag}")
    print()

    return results

# ─── Output & Save ───────────────────────────────────────────────────────────────

def display_passwords(passwords, page_size=50):
    """Display generated passwords with optional pagination."""
    section("GENERATED PATTERNS (8–9 chars only)")
    total = len(passwords)
    print(f"\n  {DM}Total: {G}{total}{DM} unique patterns{RS}\n")

    choice = input(f"  {G}▶{RS}  Show passwords now? (y/n): ").strip().lower()
    if choice != "y":
        info("Display skipped. You can still save them to a file.")
        return

    # Show first page_size then ask to continue
    for i, pw in enumerate(passwords[:page_size], 1):
        col = C if i % 2 == 0 else G
        end_char = "\n" if i % 4 == 0 else "    "
        print(f"  {DM}{i:>4}.{RS} {col}{pw:<12}{RS}", end=end_char)
    print()

    if total > page_size:
        more = input(f"\n  {G}▶{RS}  Show remaining {total - page_size} passwords? (y/n): ").strip().lower()
        if more == "y":
            for i, pw in enumerate(passwords[page_size:], page_size + 1):
                col = C if i % 2 == 0 else G
                end_char = "\n" if i % 4 == 0 else "    "
                print(f"  {DM}{i:>4}.{RS} {col}{pw:<12}{RS}", end=end_char)
            print()


def save_passwords(passwords, first, last):
    """Save all passwords to a text file."""
    fname = f"passwords_{first}_{last}.txt"
    try:
        with open(fname, "w") as f:
            f.write("=" * 60 + "\n")
            f.write("  PASSWORD PATTERN GENERATOR v2.0 — Educational Output\n")
            f.write("  DISCLAIMER: For password strength awareness only.\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"  Total passwords (8-9 chars): {len(passwords)}\n\n")
            for i, pw in enumerate(passwords, 1):
                f.write(f"{i:>5}. {pw}\n")
        ok(f"Passwords saved → {fname}")
    except OSError as e:
        err(f"Could not save: {e}")


def save_analysis(results, first, last):
    """Save analysis report to a file."""
    if not results:
        return
    fname = f"analysis_{first}_{last}.txt"
    try:
        with open(fname, "w") as f:
            f.write("=" * 60 + "\n")
            f.write("  PASSWORD ANALYSIS REPORT — Educational Output\n")
            f.write("  DISCLAIMER: For password strength awareness only.\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"  Tested Password : {'*' * len(results['password'])}\n")
            f.write(f"  Exact Match     : {'YES — CHANGE IT NOW!' if results['found'] else 'No'}\n\n")
            f.write("  Top 10 Most Similar Patterns:\n")
            f.write("  " + "-" * 40 + "\n")
            for rank, (pw, score) in enumerate(results["top10"], 1):
                f.write(f"  {rank:>2}. {pw:<14}  Similarity: {score}%\n")
        ok(f"Analysis saved  → {fname}")
    except OSError as e:
        err(f"Could not save: {e}")

# ─── Main ─────────────────────────────────────────────────────────────────────────

def main():
    clear()
    print_banner()
    print_disclaimer()

    # Step 1: Collect inputs
    data = collect_inputs()

    # Step 2: Generate passwords
    section("GENERATING PATTERNS")
    print(f"\n  {DM}Building pattern pool (8–9 chars only)...{RS}", end="", flush=True)
    passwords = generate_passwords(data, target=1000)
    print(f" {G}{len(passwords)} unique patterns ready.{RS}")

    # Step 3: Display passwords
    display_passwords(passwords)

    # Step 4: Analyze user's password
    analysis = analyze_password(passwords)

    # Step 5: Save options
    section("SAVE OPTIONS")
    print()
    if input(f"  {G}▶{RS}  Save all {len(passwords)} passwords to file? (y/n): ").strip().lower() == "y":
        save_passwords(passwords, data["first"], data["last"])

    if analysis and input(f"  {G}▶{RS}  Save analysis report to file? (y/n): ").strip().lower() == "y":
        save_analysis(analysis, data["first"], data["last"])

    # Step 6: Closing tip
    print(f"""\n{C}
  ┌─────────────────────────────────────────────────────────────┐
  │  💡 SECURITY TIP                                            │
  │  If any pattern resembles your real password, change it     │
  │  now. Use a password manager to generate a truly random     │
  │  passphrase of 16+ characters with mixed symbols.          │
  └─────────────────────────────────────────────────────────────┘{RS}\n""")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {R}[!] Interrupted. Exiting.{RS}\n")
        sys.exit(0)