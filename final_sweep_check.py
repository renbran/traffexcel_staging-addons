import sys
sys.path.insert(0, "/usr/lib/python3/dist-packages")
import odoo
import odoo.tools
import odoo.api
from odoo.modules.registry import Registry

odoo.tools.config.parse_config(["-d", "traffexcel_staging"])
r = Registry("traffexcel_staging")

with r.cursor() as cr:
    # Check for any remaining draft projects
    cr.execute("SELECT id, name, state FROM construction_project WHERE state = 'draft'")
    draft_projects = cr.fetchall()
    print("=== Remaining draft projects ===")
    for row in draft_projects:
        print("  id=%s name=%s state=%s" % row)
    
    # Check analytic accounts for cancelled projects
    cr.execute("""SELECT cp.id, cp.name, cp.state, aa.id as aa_id, aa.name as aa_name, aa.active
                  FROM construction_project cp
                  LEFT JOIN account_analytic_account aa ON aa.id = cp.analytic_account_id
                  WHERE cp.state = 'cancel'
                  ORDER BY cp.id""")
    print("\n=== Cancelled projects with analytic accounts ===")
    for row in cr.fetchall():
        print("  cp_id=%s cp_name=%s cp_state=%s aa_id=%s aa_name=%s aa_active=%s" % row)
    
    # Check for any analytic accounts that are active but linked to cancelled projects
    cr.execute("""SELECT aa.id, aa.name, aa.active, cp.id as cp_id, cp.name as cp_name, cp.state as cp_state
                  FROM account_analytic_account aa
                  JOIN construction_project cp ON cp.analytic_account_id = aa.id
                  WHERE cp.state = 'cancel' AND aa.active = TRUE""")
    print("\n=== Active analytic accounts on cancelled projects ===")
    for row in cr.fetchall():
        print("  aa_id=%s aa_name=%s aa_active=%s cp_id=%s cp_name=%s cp_state=%s" % row)
    
    # Also check for any orphaned analytic accounts (construction-related but no project link)
    cr.execute("""SELECT id, name, active FROM account_analytic_account 
                  WHERE active = TRUE 
                  AND (name ILIKE '%construction%' OR name ILIKE '%project%' 
                       OR name ILIKE '%nctc%' OR name ILIKE '%raak%' 
                       OR name ILIKE '%souq%' OR name ILIKE '%amc%' 
                       OR name ILIKE '%sharjah%' OR name ILIKE '%tunnel%' 
                       OR name ILIKE '%gantry%' OR name ILIKE '%dubai%' 
                       OR name ILIKE '%variation%' OR name ILIKE '%installation%' 
                       OR name ILIKE '%rectification%' OR name ILIKE '%cladding%' 
                       OR name ILIKE '%base%' OR name ILIKE '%traffic%' 
                       OR name ILIKE '%cultural%' OR name ILIKE '%industrial%' 
                       OR name ILIKE '%emaar%' OR name ILIKE '%flying%' 
                       OR name ILIKE '%buhaira%' OR name ILIKE '%speed%' 
                       OR name ILIKE '%jn-%' OR name ILIKE '%pc%' 
                       OR name ILIKE '%r17%' OR name ILIKE '%r19%' 
                       OR name ILIKE '%r11%' OR name ILIKE '%r17%' 
                       OR name ILIKE '%installation%' OR name ILIKE '%tunnel%'
                       OR name ILIKE '%tunnel%' OR name ILIKE '%rectification%'
                       OR name ILIKE '%cladding%' OR name ILIKE '%base%'
                       OR name ILIKE '%traffic%' OR name ILIKE '%cultural%'
                       OR name ILIKE '%industrial%' OR name ILIKE '%emaar%'
                       OR name ILIKE '%flying%' OR name ILIKE '%buhaira%'
                       OR name ILIKE '%speed%' OR name ILIKE '%jn-%'
                       OR name ILIKE '%pc%' OR name ILIKE '%r17%'
                       OR name ILIKE '%r19%' OR name ILIKE '%r11%'
                       OR name ILIKE '%r17%' OR name ILIKE '%installation%'
                       OR name ILIKE '%tunnel%' OR name ILIKE '%rectification%'
                       OR name ILIKE '%cladding%' OR name ILIKE '%base%'
                       OR name ILIKE '%traffic%' OR name ILIKE '%cultural%'
                       OR name ILIKE '%industrial%' OR name ILIKE '%emaar%'
                       OR name ILIKE '%flying%' OR name ILIKE '%buhaira%'
                       OR name ILIKE '%speed%' OR name ILIKE '%jn-%'
                       OR name ILIKE '%pc%' OR name ILIKE '%r17%')
                       ORDER BY name""")
    print("\n=== Active construction-related analytic accounts ===")
    count = 0
    for row in cr.fetchall():
        print("  id=%s name=%s active=%s" % row)
        count += 1
    print("Total:", count)