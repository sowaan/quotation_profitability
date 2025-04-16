import frappe


def profability(doc,method):


    # check_box_value = frappe.db.get_single_value('Selling Settings', 'custom_costing_rate_from_product_bundle')
    check_box_value = doc.custom_costing_rate_from_product_bundle
    if not check_box_value :
        check_box_value = 0

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
                i.custom_total_landed_per_unit_cost = sub_cost - (i.custom_item_cogs or 0)
                i.custom_dry_cost_rate_calculates_from_product_bundle_amounts = 1
        
        
        i.custom_total_landed_cost = i.custom_total_landed_per_unit_cost * i.qty
        i.custom_total_costs = i.custom_total_landed_cost + i.custom_item_cogs_cost

        totalcost = totalcost + i.custom_item_cogs_cost
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
