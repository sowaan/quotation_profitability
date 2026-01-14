import frappe


@frappe.whitelist()
def create_budget(boq_name):
    boq = frappe.get_doc("Quotation", boq_name)

    if boq.docstatus != 1:
        frappe.throw("Quotation must be submitted first")

    budget = frappe.new_doc("Budget")
    budget.company = boq.company
    budget.cost_center=boq.cost_center
    budget.custom_project=boq.project
    
    
    project = (
        getattr(boq, "project", None)
        or getattr(boq, "custom_project", None)
    )

    if project:
        budget.project = project

    budget.fiscal_year = frappe.defaults.get_user_default("fiscal_year")
    budget.budget_against = "Project"


    for row in boq.custom_budgetting:
        if row.gl_account and row.cost_amount is not None:
            budget.append("accounts", {
                "account": row.gl_account,
                "budget_amount": row.cost_amount   
            })

    budget.insert(ignore_permissions=True)

    boq.db_set("custom_budget_created", 1)

    return budget.name
