# Notepad
<!-- Auto-managed by OMC. Manual edits preserved in MANUAL section. -->

## Priority Context
<!-- ALWAYS loaded. Keep under 500 chars. Critical discoveries only. -->

## Working Memory
<!-- Session notes. Auto-pruned after 7 days. -->
### 2026-07-19 11:17
sgc_tech_ai_theme installed on demo.sgctech.ai (demo_presentation container). Key learning: Odoo 19 modules in `/mnt/extra-addons` are invisible to Manifest discovery because `odoo.addons.__path__` doesn't include extra-addons. Fix: symlink from `/usr/lib/python3/dist-packages/odoo/addons/` to `/mnt/extra-addons/`. Use `odoo module install -d <db> <module>` CLI (not MCP button_immediate_install) for installation.


## MANUAL
<!-- User content. Never auto-pruned. -->

