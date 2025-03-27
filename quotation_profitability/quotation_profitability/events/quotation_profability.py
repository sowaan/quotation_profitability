import frappe


def profability(doc,method):

    # Initialize totalcost and totaladditionalcost outside the loop
    totalcost = 0
    totaladditionalcost = 0

    # Iterate over items in doc.items
    for i in doc.items:
        # Check if i.base_rate is not zero before performing the division
        if i.base_rate != 0:
            i.custom_clearance = i.custom_clearance * (i.base_rate / 100) * i.qty
            i.custom_freight_charges = i.custom_freight_charges * (i.base_rate / 100) * i.qty
            i.custom_installation_charges = i.custom_installation_charges * i.qty
            i.custom_customs = i.custom_customs * (i.base_rate / 100) * i.qty
            i.custom_item_cogs = i.custom_item_cogs * i.qty
            i.custom_total_landed_cost = (
                i.custom_clearance+ i.custom_freight_charges + i.custom_installation_charges+ i.custom_customs
            )
            i.custom_total_costs = i.custom_total_landed_cost + i.custom_item_cogs

            # Accumulate the item cost to the totalcost
            totalcost = totalcost + i.custom_item_cogs

            # Accumulate the additional costs to totaladditionalcost
            totaladditionalcost = totaladditionalcost + i.custom_total_landed_cost 

    # Assign the totalcost to doc.custom_total_cost
    doc.custom_total_item_cogs = totalcost

    # Assuming doc.base_total is available, assign it to doc.custom_total_amount
    doc.custom_total_selling_volume = doc.base_total

    # Assign the totaladditionalcost to doc.custom_additional_costs
    doc.custom_additional_costs = totaladditionalcost

    doc.custom_gross_profit = doc.custom_total_selling_volume - doc.custom_total_item_cogs 
    doc.custom_gross_profit_percentage = doc.custom_gross_profit * 100 / doc.custom_total_selling_volume
    doc.custom_net_profit = doc.custom_gross_profit- doc.custom_additional_costs
    doc.custom_net_profit_percentage = doc.custom_net_profit * 100 / doc.custom_total_selling_volume
