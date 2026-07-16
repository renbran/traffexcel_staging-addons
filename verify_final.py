import sys
sys.path.insert(0, "/usr/lib/python3/dist-packages")
import odoo
import odoo.tools
import odoo.api
from odoo.modules.registry import Registry

odoo.tools.config.parse_config(["-d", "traffexcel_staging"])
r = Registry("traffexcel_staging")

with r.cursor() as cr:
    # Check final state
    cr.execute("SELECT COUNT(*) FROM construction_project WHERE state = 'active'")
    print("Active projects:", cr.fetchone()[0])
    
    cr.execute("SELECT COUNT(*) FROM construction_project WHERE state = 'cancel'")
    print("Cancelled projects:", cr.fetchone()[0])
    
    cr.execute("SELECT id, name, state FROM construction_project WHERE state = 'active' ORDER BY id")
    print("\n=== Active projects ===")
    for row in cr.fetchall():
        print("  %s | %s | %s" % row)
    
    cr.execute("SELECT COUNT(*) FROM account_analytic_account WHERE active = TRUE")
    print("\nTotal active analytic accounts:", cr.fetchone()[0])
    
    # Check only the 7 kept analytic accounts
    cr.execute("""SELECT id, name FROM account_analytic_account 
                  WHERE active = TRUE 
                  AND id IN (25, 27, 30, 126, 127, 129, 130)
                  ORDER BY id""")
    print("\n=== Kept analytic accounts (7) ===")
    for row in cr.fetchall():
        print("  %s | %s" % row)
    
    cr.execute("SELECT COUNT(*) FROM account_analytic_account WHERE active = FALSE")
    print("\nInactive analytic accounts:", cr.fetchone()[0])
    
    # Check if any invoices still reference cancelled projects
    cr.execute("""SELECT COUNT(*) FROM account_move 
                  WHERE construction_project_id IS NOT NULL
                    AND construction_project_id IN (
                      SELECT id FROM construction_project WHERE state = 'cancel'
                    )""")
    print("\nInvoices referencing cancelled projects:", cr.fetchone()[0])
    
    print("\n=== Sweep complete ===")