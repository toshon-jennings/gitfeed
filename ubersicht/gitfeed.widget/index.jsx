// gitfeed desktop ticker for Übersicht.
// Symlink this folder into ~/Library/Application Support/Übersicht/widgets/.
// Data comes from ../../bin/gitfeed (the same feed the menu bar uses).
import { React, run } from "uebersicht";

const h = React.createElement;

// Übersicht runs commands from its widgets folder; the symlink resolves to this repo.
export const command = "gitfeed.widget/../../bin/gitfeed";
export const refreshFrequency = 60 * 1000;

const PX_PER_SECOND = 40;

export const className = `
  left: 12px; right: 12px; bottom: 44px;
  height: 28px; overflow: hidden;
  background: #23262a; border: 1px solid #3b3f44; border-radius: 6px;
  font: 12px/28px ui-monospace, "SF Mono", Menlo, monospace;
  color: #e9e6df;
  -webkit-font-smoothing: antialiased;

  .tape { display: inline-flex; white-space: nowrap; animation: gitfeed-scroll var(--dur) linear infinite; }
  &:hover .tape { animation-play-state: paused; }
  .item { padding: 0 14px; border-right: 1px solid #3b3f44; cursor: pointer; }
  .item:hover .name { text-decoration: underline; text-underline-offset: 3px; }
  .name { font-weight: 600; }
  .age { color: #8d9298; font-size: 11px; margin-left: 8px; }
  .status { color: #e0675a; margin-left: 8px; }
  .note { padding: 0 14px; color: #8d9298; }

  @media (prefers-reduced-motion: reduce) {
    overflow-x: auto;
    .tape { animation: none; }
  }
`;

const KEYFRAMES = "@keyframes gitfeed-scroll { from { transform: translateX(0) } to { transform: translateX(-50%) } }";

const open = (url) => url && run(`open '${url.replace(/'/g, "")}'`);

const item = (r, key) =>
  h("span", { className: "item", key, title: r.full_name, onClick: () => open(r.url) },
    h("span", { className: "name" }, r.name),
    h("span", { className: "age" }, r.age),
    r.status && h("span", { className: "status" }, r.status));

export const render = ({ output, error }) => {
  let data;
  try {
    data = JSON.parse(output);
  } catch {
    return h("div", { className: "note" }, error ? `gitfeed: ${error}` : "gitfeed: loading…");
  }
  const repos = data.show_clean ? data.repos : data.repos.filter((r) => r.dirty);
  if (!repos.length) return h("div", { className: "note" }, "All repos clean");
  // Two copies side by side make the loop seamless: scrolling -50% lands exactly on the second copy.
  const dur = `${Math.max(20, repos.length * 220 / PX_PER_SECOND)}s`;
  return h("div", { className: "tape", style: { "--dur": dur } },
    h("style", null, KEYFRAMES),
    repos.map((r, i) => item(r, `a${i}`)),
    repos.map((r, i) => item(r, `b${i}`)));
};
