import sys
sys.path.insert(0, "/usr/lib/python3/dist-packages")
import odoo, odoo.tools, odoo.api
from odoo.modules.registry import Registry

odoo.tools.config.parse_config(["-d","traffexcel_staging"])
r = Registry("traffexcel_staging")
with r.cursor() as cr:
    cr.execute("SELECT COUNT(*) FROM account_analytic_line WHERE account_id IN (SELECT id FROM account_analytic_account WHERE active = FALSE)")
    print("Inactive analytic lines:", cr.fetchone()[0])
    
    cr.execute("SELECT domain FROM ir_act_window WHERE id = 154")
    print("Analytic Items domain:", cr.fetchone())
    
    cr.execute("SELECT domain FROM ir_act_window WHERE id = 156")
    print("Analytic Accounts domain:", cr.fetchone())
    
    cr.execute("SELECT domain FROM ir_act_window WHERE id = 295")
    print("Analytic Reporting domain:", cr.fetchone())