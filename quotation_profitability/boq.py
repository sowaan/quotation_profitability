import frappe
from frappe.utils import flt


def build_dry_cost_summary(doc, method=None):
    # DEBUG: confirm event firing
    # frappe.log_error(
    #     f"Dry Cost Builder Fired for {doc.doctype} {doc.name}",
    #     "DRY COST DEBUG"
    # )

    # clear target table
    profability(doc, method)
    doc.set("custom_budgetting", [])

    if not doc.items:
        return

    frappe.log_error(
        f"Next Step {doc.doctype} {doc.name}",
        "DRY COST DEBUG"
    )

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

def profability(doc,method):

    # check_box_value = frappe.db.get_single_value('Selling Settings', 'custom_costing_rate_from_product_bundle')
    check_box_value = doc.custom_costing_rate_from_product_bundle
    if not check_box_value :
        check_box_value = 0
    frappe.log_error ("check box value", f"check: {check_box_value}")
    totalcost = 0
    totaladditionalcost = 0
    
    for i in doc.items:
        sub_cost = 0
        sig = 0
        
        i.custom_dry_cost_rate_calculates_from_product_bundle_amounts = 0
        i.custom_item_cogs_cost = (i.custom_item_cogs or 0) * i.qty
        i.custom_total_landed_per_unit_cost = ( (i.custom_clearance_cost or 0) + (i.custom_freight_charges_cost or 0) + (i.custom_installation_charges_cost or 0) + (i.custom_customs_cost or 0) )
        
        if check_box_value == 1 :

            if doc.packed_items :
                for j in doc.packed_items :
                    if i.item_code == j.parent_item :
                        sub_cost = sub_cost + ( (j.custom_costing_rate or 0) * (j.qty or 0) )
                        sig = 1
            if sig == 1 :
                if i.qty > 0 :
                    i.custom_total_landed_per_unit_cost = ( sub_cost/i.qty ) - (i.custom_item_cogs or 0) 
                else :
                    i.custom_total_landed_per_unit_cost = 0
                i.custom_dry_cost_rate_calculates_from_product_bundle_amounts = 1
        
        
        i.custom_total_landed_cost = i.custom_total_landed_per_unit_cost * i.qty
        i.custom_total_costs = i.custom_total_landed_cost + i.custom_item_cogs_cost

        totalcost = totalcost + i.custom_item_cogs_cost
        frappe.log_error("I am here", f"total landed cost: {i.custom_total_landed_cost}")
        totaladditionalcost = totaladditionalcost + i.custom_total_landed_cost

    # Assign the totalcost to doc.custom_total_cost
    doc.custom_total_item_cogs = totalcost
    doc.custom_total_cogs = totalcost

    # Assuming doc.base_total is available, assign it to doc.custom_total_amount
    doc.custom_total_selling_volume = doc.base_total

    # Assign the totaladditionalcost to doc.custom_additional_costs
    doc.custom_additional_costs = totaladditionalcost
    doc.custom_total_dry_cost = totaladditionalcost

    doc.custom_gross_profit = doc.custom_total_selling_volume - doc.custom_total_item_cogs 
    doc.custom_gross_profit_percentage = doc.custom_gross_profit * 100 / doc.custom_total_selling_volume
    doc.custom_net_profit = doc.custom_gross_profit- doc.custom_additional_costs
    doc.custom_net_profit_percentage = doc.custom_net_profit * 100 / doc.custom_total_selling_volume

    doc.custom_grand_cost = doc.custom_total_dry_cost + doc.custom_total_cogs


    sum_amount = 0
    total_percent = 0
    for child in doc.custom_boq_costing_list or [] :
        sum_amount += child.amount or 0
        total_percent += child.percent or 0
    if total_percent > 100:
        frappe.throw(_("Total percentage in BOQ Costing List cannot exceed 100%."))

    doc.custom_boq_costing_total = sum_amount









