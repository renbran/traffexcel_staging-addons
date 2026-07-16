import sys
sys.path.insert(0, "/usr/lib/python3/dist-packages")
import odoo
import odoo.tools
import odoo.api
from odoo.modules.registry import Registry

odoo.tools.config.parse_config(["-d", "traffexcel_staging"])
r = Registry("traffexcel_staging")

with r.cursor() as cr:
    # The 7 projects to keep (active projects)
    keep_project_ids = [76, 72, 74, 73, 75, 77, 5]
    keep_analytic_ids = [129, 30, 127, 126, 25, 27, 130]
    
    print("=== Projects to keep ===")
    cr.execute("SELECT id, name, state FROM construction_project WHERE id IN %s", (tuple(keep_project_ids),))
    for row in cr.fetchall():
        print("  KEEP: id=%s name=%s state=%s" % row)
    
    print("\n=== Projects to archive ===")
    cr.execute("SELECT id, name, state FROM construction_project WHERE id NOT IN %s", (tuple(keep_project_ids),))
    to_archive = cr.fetchall()
    for row in to_archive:
        print("  ARCHIVE: id=%s name=%s state=%s" % row)
    
    # Archive projects not in keep list
    cr.execute("UPDATE construction_project SET active = FALSE WHERE id NOT IN %s", (tuple(keep_project_ids),))
    print("\nArchived %d projects" % len(to_archive))
    
    print("\n=== Analytic accounts to keep ===")
    cr.execute("SELECT id, name FROM account_analytic_account WHERE id IN %s", (tuple(keep_analytic_ids),))
    for row in cr.fetchall():
        print("  KEEP: id=%s name=%s" % row)
    
    print("\n=== Analytic accounts to archive ===")
    cr.execute("SELECT id, name FROM account_analytic_account WHERE id NOT IN %s AND name ILIKE '%%construction%%' OR name ILIKE '%%project%%' OR name ILIKE '%%nctc%%' OR name ILIKE '%%raak%%' OR name ILIKE '%%souq%%' OR name ILIKE '%%amc%%' OR name ILIKE '%%sharjah%%' OR name ILIKE '%%tunnel%%' OR name ILIKE '%%gantry%%' OR name ILIKE '%%dubai%%' OR name ILIKE '%%variation%%' OR name ILIKE '%%installation%%' OR name ILIKE '%%rectification%%' OR name ILIKE '%%cladding%%' OR name ILIKE '%%base%%' OR name ILIKE '%%traffic%%' OR name ILIKE '%%cultural%%' OR name ILIKE '%%industrial%%' OR name ILIKE '%%emaar%%' OR name ILIKE '%%flying%%' OR name ILIKE '%%buhaira%%' OR name ILIKE '%%speed%%' OR name ILIKE '%%jn-%' OR name ILIKE '%%pc%' OR name ILIKE '%%r17%' OR name ILIKE '%%r19%' OR name ILIKE '%%r11%' OR name ILIKE '%%r17%'", )
    to_archive_aa = cr.fetchall()
    for row in to_archive_aa:
        print("  ARCHIVE AA: id=%s name=%s" % row)
    
    # Archive the construction-related analytic accounts not in keep list
    cr.execute("""UPDATE account_analytic_account 
                  SET active = FALSE 
                  WHERE id NOT IN %s 
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
                         OR name ILIKE '%r11%' OR name ILIKE '%r17%')""", (tuple(keep_analytic_ids),))
    print("\nArchived construction-related analytic accounts not in keep list")
    
    # Also archive uploaded files/attachments for archived projects
    cr.execute("""SELECT ir_attachment.id FROM ir_attachment
                  JOIN construction_project cp ON ir_attachment.res_model = 'construction.project' AND ir_attachment.res_id = cp.id
                  WHERE cp.id NOT IN %s""", (tuple(keep_project_ids),))
    attachment_ids = [row[0] for row in cr.fetchall()]
    if attachment_ids:
        cr.execute("UPDATE ir_attachment SET active = FALSE WHERE id IN %s", (tuple(attachment_ids),))
        print("\nArchived %d attachments for archived projects" % len(attachment_ids))
    
    cr.commit()
    print("\n=== Cleanup complete ===")