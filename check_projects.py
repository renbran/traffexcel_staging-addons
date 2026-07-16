import sys
sys.path.insert(0, "/usr/lib/python3/dist-packages")
import odoo
import odoo.tools
import odoo.api
from odoo.modules.registry import Registry

odoo.tools.config.parse_config(["-d","traffexcel_staging"])
r = Registry("traffexcel_staging")
with r.cursor() as cr:
    # Get all construction projects with their analytic accounts
    cr.execute("""SELECT cp.id, cp.name, cp.state, cp.analytic_account_id, 
                         aa.name as analytic_name,
                         COUNT(am.id) as invoice_count
                  FROM construction_project cp
                  LEFT JOIN account_analytic_account aa ON aa.id = cp.analytic_account_id
                  LEFT JOIN account_move am ON am.move_type IN ('out_invoice','in_invoice','out_refund','in_refund') 
                      AND am.construction_project_id = cp.id
                  GROUP BY cp.id, cp.name, cp.state, cp.analytic_account_id, aa.name
                  ORDER BY invoice_count DESC""")
    print("=== Construction Projects ===")
    for row in cr.fetchall():
        print("  id=%s name=%s state=%s analytic_id=%s analytic_name=%s invoices=%s" % row)
    
    # Also check analytic accounts in accounting
    cr.execute("""SELECT aa.id, aa.name, aa.company_id 
                  FROM account_analytic_account aa
                  WHERE aa.name ILIKE '%construction%' OR aa.name ILIKE '%project%'
                  ORDER BY aa.name""")
    print("\n=== Analytic Accounts (construction/project) ===")
    for row in cr.fetchall():
        print("  id=%s name=%s company_id=%s" % row)