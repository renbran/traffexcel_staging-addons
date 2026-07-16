import sys
sys.path.insert(0, "/usr/lib/python3/dist-packages")
import odoo
import odoo.tools
import odoo.api
from odoo.modules.registry import Registry

odoo.tools.config.parse_config(["-d","traffexcel_staging"])
r = Registry("traffexcel_staging")
with r.cursor() as cr:
    cr.execute("""SELECT imd.name, imd.model, imd.res_id
                   FROM ir_model_data imd
                   WHERE imd.module IN ('sgc_construction_analytic_enhanced','sgc_construction_management','account')
                     AND imd.model IN ('ir.ui.view','ir.actions.act_window','ir.ui.menu')
                     AND imd.name ILIKE '%analytic%'
                   ORDER BY imd.name""")
    for row in cr.fetchall():
        print("  Analytic-related:", row)