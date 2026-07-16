import sys
sys.path.insert(0, "/usr/lib/python3/dist-packages")
import odoo
import odoo.tools
import odoo.api
from odoo.modules.registry import Registry

odoo.tools.config.parse_config(["-d","traffexcel_staging"])
r = Registry("traffexcel_staging")
with r.cursor() as cr:
    cr.execute("SELECT column_name FROM information_schema.columns WHERE table_name=%s", ("construction_project",))
    for row in cr.fetchall():
        print(row[0])