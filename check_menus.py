import sys
sys.path.insert(0, "/usr/lib/python3/dist-packages")
import odoo, odoo.tools, odoo.api
from odoo.modules.registry import Registry

odoo.tools.config.parse_config(["-d","traffexcel_staging"])
r = Registry("traffexcel_staging")
with r.cursor() as cr:
    cr.execute("""SELECT imd.name, imd.model, imd.res_id, menu.name as menu_name
                   FROM ir_model_data imd
                   JOIN ir_ui_menu menu ON menu.id = imd.res_id
                   WHERE imd.module IN ('sgc_construction_analytic_enhanced','sgc_construction_management')
                     AND imd.model = 'ir.ui.menu'
                   ORDER BY menu.name""")
    for row in cr.fetchall():
        print("  Menu:", row)
    
    cr.execute("""SELECT imd.name, imd.model, imd.res_id
                   FROM ir_model_data imd
                   WHERE imd.module IN ('sgc_construction_analytic_enhanced','sgc_construction_management')
                     AND imd.model = 'ir.actions.act_window'
                   ORDER BY imd.name""")
    for row in cr.fetchall():
        print("  Action:", row)