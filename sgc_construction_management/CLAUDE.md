# sgc_construction_management — LIVE, SHARED, HIGH-RISK MODULE

This directory is served **live** to `staging.sgctech.ai` (container `staging-traffexcel`,
DB `traffexcel_staging`, bind-mounted read-write from `/opt/merged-addons` into
`/mnt/extra-addons`). Real users hit this module every day (Construction app: Dashboard,
Projects, BOQ, Billing, etc.). There is no separate "dev copy" — whatever is on disk here
is one `-u sgc_construction_management` away from being pushed live.

## Do not edit this module casually

**On 2026-07-18, a commit intended as a narrow "report header/footer layout" fix
instead silently overwrote 55 files (2378 deletions / 511 insertions) with an
unrelated, months-old snapshot of this module** — reverting the analytics
dashboard, dropping the `outstanding_balance` field, and breaking the live site
with a client-side OwlError for a full week before anyone noticed. See git log
`0c154de` and `6449ec8` on branch `deploy-tmp` for the recovery, and
`origin/backup/local-main-20260719-preserve-analytics` (commit `ffdf145`) for the
last-known-good reference state.

**Before touching any file in this directory:**

1. **Scope your diff to this module only.** Never run a bulk `git checkout <ref> -- .`,
   `rsync`, `tar -x`, or "restore from backup" operation from the repo root or a
   parent directory — always target `sgc_construction_management/` explicitly, and
   review `git diff --stat` for this module BEFORE committing. If the diff touches
   more than the files you intentionally changed, stop and investigate — do not
   commit it.
2. **Never blindly trust `/opt/merged-addons`'s working tree as "current."** Other
   copies of this module exist on this host (`/opt/deploy/extra-addons`,
   `/opt/odoo-prod/extra-addons`, `/opt/odoo-prod/backups/*`) with *different,
   sometimes newer* versions (`__manifest__.py` version strings do not always
   agree — compare them before assuming which copy is authoritative).
3. **A module upgrade (`-u sgc_construction_management`) alone is not enough**
   when a Python model field (`models/*.py`) was added, removed, or renamed.
   The running Odoo server workers do NOT re-import Python source on `-u` — only
   a one-off process does. After any model-field change, the live container
   (`staging-traffexcel`) must be **restarted** (`docker restart staging-traffexcel`)
   or the running workers will keep serving stale field definitions while the
   database and one-off processes see the new ones — causing exactly this kind
   of view/model mismatch crash.
4. **Any real, intentional change requires:**
   - A version bump in `__manifest__.py` (`version` key).
   - An explicit, scoped commit message (not an anonymous autopush).
   - A test load of the Construction app in a browser (Dashboard, Projects list,
     Projects kanban, at minimum) before considering the change done.
5. **The `/opt/merged-addons` autopush cron for this repo is currently commented
   out** in `crontab -l` (`# */5 * * * * .../autopush.sh /opt/merged-addons
   traffexcel_staging-addons`). If you re-enable it, understand that it will
   auto-commit and auto-push *anything* sitting in the working tree every 5
   minutes with zero review — exactly the mechanism that let the 2026-07-18
   regression reach `origin/deploy-tmp` unnoticed.

## If an AI agent is asked to "just fix X" here

Make the smallest possible diff. If your fix requires touching more than the
specific file(s) relevant to X, stop and ask the user for confirmation before
committing — do not assume a full-directory restore, extraction, or copy is
the right tool. When in doubt, `git diff --stat` your staged changes against
this module's known-good reference (`ffdf145` / `backup/local-main-20260719-preserve-analytics`)
before pushing.
