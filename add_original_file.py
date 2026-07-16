import sys
sys.path.insert(0, "/usr/lib/python3/dist-packages")
import odoo
import odoo.tools
import odoo.api
from odoo.modules.registry import Registry

odoo.tools.config.parse_config(["-d", "traffexcel_staging"])
r = Registry("traffexcel_staging")

with r.cursor() as cr:
    # Check current columns
    cr.execute("SELECT column_name FROM information_schema.columns WHERE table_name='construction_project_photo' AND column_name LIKE 'original%'")
    existing = [row[0] for row in cr.fetchall()]
    print("Existing original columns: %s" % existing)

    # Add original_file column if missing
    if "original_file" not in existing:
        cr.execute("ALTER TABLE construction_project_photo ADD COLUMN original_file bytea")
        print("Added original_file column")
    else:
        print("original_file already exists")

    # Verify
    cr.execute("SELECT column_name FROM information_schema.columns WHERE table_name='construction_project_photo' AND column_name LIKE 'original%'")
    print("Now: %s" % [row[0] for row in cr.fetchall()])
    cr.commit()