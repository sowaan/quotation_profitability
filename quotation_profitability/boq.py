import frappe
from frappe.utils import flt


def build_dry_cost_summary(doc, method=None):
    # DEBUG: confirm event firing
    frappe.log_error(
        f"Dry Cost Builder Fired for {doc.doctype} {doc.name}",
        "DRY COST DEBUG"
    )

    # clear target table
    doc.set("custom_budgetting", [])

    if not doc.items:
        return

    grouped = {}

   
    for row in doc.items:
        if not row.item_group:
            continue

        amount = flt(row.custom_total_landed_cost or 0)
        #if amount <= 0:
            # continue

        if row.item_group not in grouped:
            grouped[row.item_group] = {
                "total": 0,
                "gl": get_item_group_gl(row.item_group, doc.company)
            }

        grouped[row.item_group]["total"] += amount

   
    for item_group, data in grouped.items():
        doc.append("custom_budgetting", {
            "item_group": item_group,
            "gl_account": data["gl"],
            "cost_amount": data["total"]
        })


def get_item_group_gl(item_group, company):
    return frappe.db.get_value(
        "Item Default",
        {
            "parent": item_group,
            "company": company
        },
        "expense_account"
    )
