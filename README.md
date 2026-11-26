# gitfeed

A ticker of your GitHub repos, newest activity first. Each entry shows how long ago it was last
committed and, for checkouts under `~/projects`, what's still waiting in the working tree. It
appears in two places, both fed by the same data:

- **Menu bar** (SwiftBar): one width-capped line that cycles through repos. Click it for the full
  list; click a repo to open it on GitHub. Hold ⌥ to open the local folder in Finder instead.
- **Desktop** (Übersicht): a thin strip that scrolls just above the Dock, behind your windows.
  Hover to pause it; click a name to open the repo.

## Status glyphs

Same shorthand as `git status -s`:

| Glyph | Meaning |
|---|---|
| `+3` | staged, not committed |
| `~3` | modified, not staged |
| `?3` | untracked files |
| `↑3` | commits not pushed |
| `↓3` | commits on the remote you haven't pulled |

No glyph means the checkout is clean, or the repo isn't checked out locally.

## Setup

```bash
brew install --cask swiftbar ubersicht
```

Open both apps once (SwiftBar asks for a plugin folder), then:

```bash
./install.sh
```

Requires `gh` signed in (`gh auth status`) and Homebrew Python at `/opt/homebrew/bin/python3`.

## Options

Config lives in `~/.config/gitfeed/config.json` (created on first change):

| Key | Default | |
|---|---|---|
| `show_clean` | `true` | Include clean repos in the cycle. Toggle from the menu bar dropdown or `bin/gitfeed toggle-clean`. |
| `roots` | `["~/projects"]` | Folders scanned for local checkouts. |
| `max_repos` | `40` | Cap on clean repos shown. Repos with pending work are always shown. |

GitHub data is cached for 10 minutes in `~/.cache/gitfeed/`; local status is read fresh every minute.
The desktop strip sits 44px above the screen bottom to clear a small bottom Dock. Change
`bottom:` in `ubersicht/gitfeed.widget/index.jsx` if yours differs.

## Layout

| Path | Role |
|---|---|
| `bin/gitfeed` | Builds the JSON feed (`gh api graphql` + `git status`). The only data source. |
| `swiftbar/gitfeed.1m.py` | Menu bar plugin; refreshes every minute. |
| `ubersicht/gitfeed.widget/index.jsx` | Desktop ticker widget. |
| `install.sh` | Symlinks the two front-ends into their apps. |
