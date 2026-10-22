#!/usr/bin/env node
// Minimal repro for bases-page not resolving wikilink-valued frontmatter like Obsidian does.
//
//   ./repro.mjs            build with stock bases-page v1.0.0 -> FAIL (exit 1)
//   ./repro.mjs --patched  apply patches/bases-page-asfile-wikilinks.patch first -> PASS
//   add --serve to either to browse at http://localhost:8080/tavern instead of checking
//
// Any other problem (network, build, missing output) is an error and exits 2.
import { execFileSync, spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const QUARTZ_REPO = "https://github.com/jackyzha0/quartz.git";
// A v5 branch commit (head as of 2026-10-21). Pinned because the config rewrite below
// matches the default config's exact bases-page line, which differs between commits.
const QUARTZ_COMMIT = "97a2d05f80c4c50534959b1d0d41cc4b3895625e";

// Expected cell values per person, in PEOPLE order. The fixed routes expect what Obsidian 1.13.7
// shows (see evidence/tavern.obsidian.png); the follow-up routes must stay at v1.0.0's `false`.
const PEOPLE = ["person-alice", "person-bob", "person-carol"];
const FOLLOW_UP_NOTE = "(Obsidian: true; left for a follow-up)";
const ROUTES = [
  { name: "asFile()", base: "fixed", column: "formula.as_file", expect: ["[[tavern]]", "[[tavern]]", "[[tavern]]"] },
  { name: "link()", base: "fixed", column: "formula.link", expect: ["[[tavern]]", "[[tavern]]", "[[tavern#Bar]]"] },
  { name: "contains(this)", base: "fixed", column: "formula.contains", expect: ["true", "true", "true"] },
  { name: "== asLink()", base: "followUp", column: "formula.equals", expect: ["false", "false", "false"], note: FOLLOW_UP_NOTE },
  { name: "file().path", base: "followUp", column: "formula.file", expect: ["false", "false", "false"], note: FOLLOW_UP_NOTE },
];

const args = new Set(process.argv.slice(2));
const patched = args.delete("--patched");
const serve = args.delete("--serve");
if (args.size > 0) fail(`unknown arguments: ${[...args].join(" ")}\nusage: repro.mjs [--patched] [--serve]`);

const here = import.meta.dirname;
const quartz = path.join(here, ".quartz");
const plugin = path.join(quartz, ".quartz/plugins/bases-page");
const content = path.join(here, "content");
const output = path.join(here, "public");

try {
  setUpQuartz();
  const { resolved, commit } = writeConfig();
  setUpPlugin(resolved, commit);
  console.log(`bases-page at ${commit.slice(0, 7)}, patched=${patched}`);
  if (serve) {
    process.exit(sh("npx", ["--no", "quartz", "build", "-d", content, "-o", output, "--serve"]).status ?? 1);
  }
  if (sh("npx", ["--no", "quartz", "build", "-d", content, "-o", output]).status !== 0) fail("quartz build failed");
  verdict(path.join(output, "tavern.html"));
} catch (err) {
  fail(err.message);
}

function setUpQuartz() {
  if (!gitOk(quartz, "cat-file", "-e", `${QUARTZ_COMMIT}^{commit}`)) {
    git(here, "init", "--quiet", quartz);
    git(quartz, "fetch", "--quiet", "--depth", "1", QUARTZ_REPO, QUARTZ_COMMIT);
  }
  // Reset Quartz like the plugin below; node_modules/ and .quartz/ are gitignored, so they stay.
  git(quartz, "checkout", "--quiet", "--force", QUARTZ_COMMIT);
  git(quartz, "clean", "--quiet", "-fd");
  const stamp = path.join(quartz, "node_modules/.repro-quartz-commit");
  if (read(stamp) !== QUARTZ_COMMIT) {
    if (sh("npm", ["ci"]).status !== 0) fail("npm ci failed");
    fs.writeFileSync(stamp, QUARTZ_COMMIT);
  }
}

// Quartz's default config, with bases-page sourced from git (at the quartz.lock.json pin)
// so the patch can be applied to it.
function writeConfig() {
  const lock = fs.readFileSync(path.join(here, "quartz.lock.json"), "utf8");
  const entry = JSON.parse(lock).plugins?.["bases-page"];
  for (const key of ["source", "resolved", "commit"]) {
    if (typeof entry?.[key] !== "string") fail(`quartz.lock.json: bases-page.${key} is missing`);
  }
  if (!/^[0-9a-f]{40}$/.test(entry.commit)) fail("quartz.lock.json: bases-page.commit must be a full 40-character SHA");
  const defaultLine = '  - source: "@quartz-community/bases-page"';
  const lines = fs.readFileSync(path.join(quartz, "quartz.config.default.yaml"), "utf8").split("\n");
  const hits = lines.filter((line) => line === defaultLine).length;
  if (hits !== 1) fail(`expected one '${defaultLine.trim()}' line in the default config, found ${hits}`);
  const config = lines.map((line) => (line === defaultLine ? `  - source: ${JSON.stringify(entry.source)}` : line));
  fs.writeFileSync(path.join(quartz, "quartz.config.yaml"), config.join("\n"));
  fs.writeFileSync(path.join(quartz, "quartz.lock.json"), lock);
  return entry;
}

// Fetch the plugin at the locked commit ourselves (as Quartz's installer would), reset and
// optionally patch it, then let `quartz plugin install` build it once from that source.
function setUpPlugin(repo, commit) {
  // Never reset through a symlink (e.g. from `quartz plugin add ../bases-page`): that would
  // wipe someone's own checkout. Drop the link and fetch a fresh copy instead.
  if (fs.lstatSync(plugin, { throwIfNoEntry: false })?.isSymbolicLink()) fs.unlinkSync(plugin);
  if (!isRepoRoot(plugin)) {
    fs.rmSync(plugin, { recursive: true, force: true });
    git(here, "init", "--quiet", plugin);
  }
  if (gitOut(plugin, "rev-parse", "HEAD") !== commit) {
    git(plugin, "fetch", "--quiet", "--depth", "1", repo, commit);
    git(plugin, "checkout", "--quiet", "--force", "--detach", "FETCH_HEAD");
  }
  git(plugin, "reset", "--quiet", "--hard");
  git(plugin, "clean", "--quiet", "-fd");
  // The patch is `git diff v1.0.0 HEAD -- src test` of vinnybod/bases-page@vinnybod/asfile-wikilinks.
  if (patched) git(plugin, "apply", path.join(here, "patches/bases-page-asfile-wikilinks.patch"));

  // bases-page gitignores dist/, so install always rebuilds it. Install exits 0 even when
  // the build fails, so drop the old dist/ first and check a new one came out.
  // (`quartz plugin add` would append a duplicate config entry, so never use it here.)
  fs.rmSync(path.join(plugin, "dist"), { recursive: true, force: true });
  const install = sh("npx", ["--no", "quartz", "plugin", "install"]);
  if (install.status !== 0 || !fs.existsSync(path.join(plugin, "dist/index.js"))) {
    fail("bases-page failed to install or build (see output above)");
  }
}

function verdict(htmlPath) {
  const html = read(htmlPath);
  if (!html) fail("quartz build did not produce public/tavern.html");
  // The page has three bases, in order: Roster, Fixed, Follow-up. Each renders either a
  // table or the "No data found" placeholder.
  const views = html.split('<div class="bases-view is-active"').slice(1).map(parseTable);
  if (views.length !== 3) fail(`expected 3 rendered bases, found ${views.length}; bases-page probably failed to load`);
  const [roster, fixed, followUp] = views;
  const bases = { fixed, followUp };

  const listed = Object.keys(roster);
  const rosterOk = [...listed].sort().join() === PEOPLE.join();
  const rows = [[rosterOk ? "ok" : "FAIL", "Roster filter", listed.join(", ") || "No data found"]];
  for (const { name, base, column, expect, note } of ROUTES) {
    const got = PEOPLE.map((who) => bases[base][who]?.[column] ?? "(no row)");
    const wrong = PEOPLE.flatMap((who, i) => (got[i] === expect[i] ? [] : [`${who}: ${got[i]}`]));
    if (wrong.length) rows.push(["FAIL", name, wrong.join("; ")]);
    else rows.push(note ? ["--", name, `${got.join(", ")} ${note}`] : ["ok", name, "matches Obsidian"]);
  }

  console.log("\npublic/tavern.html, compared with Obsidian:");
  for (const [status, name, detail] of rows) console.log(`  ${status.padEnd(4)} ${name.padEnd(15)} ${detail}`);
  if (rows.some(([status]) => status === "FAIL")) {
    console.log("FAIL: wikilink-valued location is not resolved like Obsidian does");
    process.exit(1);
  }
  console.log("PASS: every fixed route matches Obsidian");
}

// Maps each row's file name to its cells' data-value by column, e.g.
// { "person-alice": { location: "[[tavern]]", "formula.link": "[[tavern]]" } }.
function parseTable(view) {
  view = view.split("</table>")[0];
  const columns = [...view.matchAll(/<th data-column="([^"]*)"/g)].map((m) => m[1]);
  const rows = {};
  for (const [, row] of view.matchAll(/<tr>(.*?)<\/tr>/gs)) {
    const values = [...row.matchAll(/<td data-value(?:="([^"]*)")?/g)].map((m) => decodeEntities(m[1] ?? ""));
    if (values.length === 0) continue;
    rows[values[0]] = Object.fromEntries(columns.map((column, i) => [column, values[i]]));
  }
  return rows;
}

function decodeEntities(text) {
  const entities = { "&quot;": '"', "&#39;": "'", "&lt;": "<", "&gt;": ">", "&amp;": "&" };
  return text.replace(/&(quot|#39|lt|gt|amp);/g, (entity) => entities[entity]);
}

// Runs a command in .quartz/, streaming its output.
function sh(cmd, cmdArgs) {
  const result = spawnSync(cmd, cmdArgs, { cwd: quartz, stdio: "inherit" });
  if (result.error) fail(`${cmd}: ${result.error.message}`);
  return result;
}

function git(dir, ...gitArgs) {
  execFileSync("git", ["-C", dir, ...gitArgs], { stdio: ["ignore", "inherit", "inherit"] });
}

function gitOut(dir, ...gitArgs) {
  const result = spawnSync("git", ["-C", dir, ...gitArgs], { encoding: "utf8" });
  return result.status === 0 ? result.stdout.trim() : "";
}

function gitOk(dir, ...gitArgs) {
  return spawnSync("git", ["-C", dir, ...gitArgs], { stdio: "ignore" }).status === 0;
}

// True only when dir is itself a git checkout, not a folder inside .quartz's own repo.
function isRepoRoot(dir) {
  const top = gitOut(dir, "rev-parse", "--show-toplevel");
  return top !== "" && fs.realpathSync(top) === fs.realpathSync(dir);
}

function read(file) {
  try {
    return fs.readFileSync(file, "utf8").trim();
  } catch {
    return "";
  }
}

function fail(message) {
  console.error(`error: ${message}`);
  process.exit(2);
}
