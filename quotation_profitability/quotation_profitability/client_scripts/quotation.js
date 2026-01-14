frappe.ui.form.on('Quotation', {
    refresh: function (frm) {
        console.log('_ora soft');
        // Ensure packed_items exists before trying to iterate
        if (frm.doc.packed_items && frm.doc.packed_items.length > 0) {
            frm.doc.packed_items.forEach((packed_item) => {
                // Check if packed item exists, has an item_code, and custom_costing_rate is not already set
                if (packed_item.item_code && (!packed_item.custom_costing_rate || packed_item.custom_costing_rate === 0)) {
                    frappe.call({
                        method: "frappe.client.get_list",
                        args: {
                            doctype: "Item Price",
                            filters: {
                                item_code: packed_item.item_code,
                                price_list: "Standard Buying",
                                valid_from: ["<=", frm.doc.transaction_date]
                            },
                            fields: ["price_list_rate", "valid_from"],
                            order_by: "valid_from desc",
                            limit_page_length: 1
                        },
                        callback: function (r) {
                            if (r.message && r.message.length > 0) {
                                const item_price = r.message[0];
                                frappe.model.set_value(packed_item.doctype, packed_item.name, 'custom_costing_rate', item_price.price_list_rate);
                            } else {
                                frappe.model.set_value(packed_item.doctype, packed_item.name, 'custom_costing_rate', 0);
                            }
                        }
                    });
                }
            });
        }
       if (frm.doc.docstatus === 1 && !frm.doc.custom_budget_created) {
            frm.add_custom_button(
                __("Create Budget"),
                function () {
                    create_budget_from_quotation(frm);
                },
                __("Create")
            );
        }
    },

    custom_costing_rate_from_product_bundle: function (frm) {
        if (frm.doc.custom_costing_rate_from_product_bundle == 1) {
            if (frm.doc.items) {
                frm.doc.items.forEach(x => {
                    frappe.model.set_value(x.doctype, x.name, "custom_clearance_cost", 0);
                    frappe.model.set_value(x.doctype, x.name, "custom_freight_charges_cost", 0);
                    frappe.model.set_value(x.doctype, x.name, "custom_installation_charges_cost", 0);
                    frappe.model.set_value(x.doctype, x.name, "custom_customs_cost", 0);
                    // Optionally make fields read-only
                    // frappe.model.set_value(x.doctype, x.name, "custom_make_fields_read_only", 1);
                });
                frm.fields_dict["items"].grid.refresh();
            }
        } else {
            if (frm.doc.items) {
                frm.doc.items.forEach(x => {
                    frappe.model.set_value(x.doctype, x.name, "custom_make_fields_read_only", 0);
                });
                frm.fields_dict["items"].grid.refresh();
            }
        }
    },

});

function create_budget_from_quotation(frm) {
    if (!frm.doc.custom_budgetting || frm.doc.custom_budgetting.length === 0) {
        frappe.msgprint(__("No budget lines found."));
        return;
    }

    if (!frm.doc.custom_project) {
        frappe.msgprint(__("Project is mandatory to create Budget"));
        return;
    }


    frappe.call({
        method: "frappe.client.insert",
        args: {
            doc: {
                doctype: "Budget",
                company: frm.doc.company,
                fiscal_year: "2026", //frappe.defaults.get_user_default("fiscal_year"),
                // fiscal_year: frappe.defaults.get_user_default("fiscal_year"),
                budget_against: "Project",
                project: frm.doc.custom_project,

                accounts: frm.doc.custom_budgetting.map(row => ({
                    account: row.gl_account,
                    budget_amount: row.cost_amount,
                    // project: frm.doc.custom_project   // 🔴 THIS WAS MISSING
                }))
            }
        },
        // callback: function (r) {
        //     if (!r.exc) {
        //         frappe.msgprint(__("Budget created successfully"));
        //         frappe.set_route("Form", "Budget", r.message.name);
        //     }
        // }
        callback: function (r) {
    if (!r.exc) {
        frappe.msgprint(__("Budget created successfully"));

        // mark quotation
        frappe.db.set_value(
            "Quotation",
            frm.doc.name,
            "custom_budget_created",
            1
        );

        frappe.set_route("Form", "Budget", r.message.name);
    }
}

    });
}