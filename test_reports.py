import sys
sys.path.insert(0, "/usr/lib/python3/dist-packages")
import odoo
import odoo.tools
import odoo.api
from odoo.modules.registry import Registry

odoo.tools.config.parse_config(["-d", "traffexcel_staging"])
r = Registry("traffexcel_staging")
with r.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    SoA = env["report.sgc_construction_analytic_enhanced.report_soa_summary"]
    projects = env["construction.project"].search([("id", "in", [5,72,73,74,75,76,77])])
    result = SoA._get_report_values(projects.ids)
    print("SOA Summary report_data keys:", list(result["report_data"].keys()))
    for pid, data in result["report_data"].items():
        print(f"  Project {pid}: invoices={len(data.get('invoices',[]))}, bills={len(data.get('bills',[]))}")

    ProjectSOA = env["report.sgc_construction_management.report_project_soa"]
    result2 = ProjectSOA._get_report_values([p.id for p in projects])
    print("\nProject SOA report_data keys:", list(result2["report_data"].keys()))
    for pid, data in result2["report_data"].items():
        print(f"  Project {pid}: invoices={len(data.get('invoices',[]))}, bills={len(data.get('bills',[]))}")