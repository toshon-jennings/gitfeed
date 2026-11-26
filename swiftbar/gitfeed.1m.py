#!/opt/homebrew/bin/python3
# <swiftbar.title>gitfeed</swiftbar.title>
# <swiftbar.desc>Cycles through your GitHub repos with last-commit age and local git status.</swiftbar.desc>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>true</swiftbar.hideSwiftBar>
"""SwiftBar plugin. Symlink into your SwiftBar plugin folder; it reads ../bin/gitfeed."""
import json, os, subprocess, sys

GITFEED = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "bin", "gitfeed")
GITFEED = os.path.normpath(GITFEED)
ICON = ":arrow.triangle.branch:"
TITLE_LEN = 30  # hard cap on menu bar width, in characters
MENU = "font=Menlo size=12"

try:
    data = json.loads(subprocess.run([sys.executable, GITFEED], capture_output=True, text=True,
                                     timeout=60, check=True).stdout)
except Exception as e:
    print(f"{ICON} ! | color=#c0392b")
    print("---")
    print(f"gitfeed failed: {e}")
    print("Refresh | refresh=true")
    sys.exit()

repos = data["repos"]
cycle = repos if data["show_clean"] else [r for r in repos if r["dirty"]]


def link(r):
    return f"href={r['url']}" if r["url"] else ""


# Header: SwiftBar rotates every line above the first '---'.
if cycle:
    for r in cycle:
        print(f"{ICON} {' '.join(x for x in (r['name'], r['age'], r['status']) if x)} "
              f"| length={TITLE_LEN} {link(r)}")
else:
    print(ICON)

print("---")
if data["error"]:
    print(f"{data['error']} | color=#c0392b")

width = max((len(r["name"]) for r in repos), default=0)
for r in repos:
    line = f"{r['name'].ljust(width)}  {r['age'].rjust(3)}  {r['status']}".rstrip()
    print(f"{line} | {MENU} {link(r)}")
    if r["local"]:  # hold ⌥ to open the checkout in Finder instead
        print(f"{line}  ⌥ open folder | {MENU} alternate=true bash=/usr/bin/open "
              f"param1={r['local']['path']} terminal=false")

print("---")
print(f"Show clean repos in cycle | checked={str(data['show_clean']).lower()} "
      f"bash={sys.executable} param1={GITFEED} param2=toggle-clean terminal=false refresh=true")
print("Refresh now | refresh=true")
