#!/usr/bin/env python3
# <swiftbar.title>gitfeed</swiftbar.title>
# <swiftbar.desc>Cycles through your GitHub repos with last-commit age and local git status.</swiftbar.desc>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>
"""SwiftBar plugin. Symlink into your SwiftBar plugin folder; it reads ../bin/gitfeed."""
import base64, json, os, subprocess, sys

GITFEED = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "bin", "gitfeed")
GITFEED = os.path.normpath(GITFEED)
HERE = os.path.dirname(os.path.realpath(__file__))
# gitfeed mark (docs/logo-template.svg), as a template image so macOS tints it for light/dark menu bars
with open(os.path.join(HERE, "icon.png"), "rb") as f:
    ICON = "templateImage=" + base64.b64encode(f.read()).decode()
TITLE_LEN = 30  # hard cap on menu bar width, in characters
MENU = "font=Menlo size=12"

try:
    data = json.loads(subprocess.run([sys.executable, GITFEED], capture_output=True, text=True,
                                     timeout=60, check=True).stdout)
except Exception as e:
    print(f"! | color=#c0392b {ICON}")
    print("---")
    print(f"gitfeed failed: {e}")
    print("Refresh | refresh=true")
    sys.exit()

repos = data["repos"]
cycle = repos if data["show_clean"] else [r for r in repos if r["dirty"]]


def text(v):
    """Text shown before '|': a '|' or newline in it would start SwiftBar parameters or a new item."""
    return " ".join(str(v).replace("|", "¦").split())


def quoted(v):
    """Parameter value after '|', in SwiftBar's quoted form so spaces and '=' stay inside it.
    None when the value can't be carried safely (a '|', newline, quote or backslash)."""
    v = str(v)
    if any(c in v for c in '|\n\r"\\'):  # don't rely on SwiftBar's escape handling
        return None
    return f'"{v}"'


def link(r):
    url = r["url"] and quoted(r["url"])
    return f"href={url}" if url else ""


# Header: SwiftBar rotates every line above the first '---'.
if cycle:
    for r in cycle:
        print(f"{text(' '.join(x for x in (r['name'], r['age'], r['status']) if x))} "
              f"| length={TITLE_LEN} {ICON}")
else:
    print(f" | {ICON}")

print("---")
if data["error"]:
    print(f"{text(data['error'])} | color=#c0392b")

width = max((len(text(r["name"])) for r in repos), default=0)
for r in repos:
    line = f"{text(r['name']).ljust(width)}  {r['age'].rjust(3)}  {r['status']}".rstrip()
    print(f"{line} | {MENU} {link(r)}")
    path = r["local"] and quoted(r["local"]["path"])
    if path:  # hold ⌥ to open the checkout in Finder instead
        print(f"{line}  ⌥ open folder | {MENU} alternate=true bash=/usr/bin/open param1={path} terminal=false")

print("---")
print(f"Show clean repos in cycle | checked={str(data['show_clean']).lower()} "
      f"bash={quoted(sys.executable)} param1={quoted(GITFEED)} param2=toggle-clean terminal=false refresh=true")
print("Refresh now | refresh=true")
