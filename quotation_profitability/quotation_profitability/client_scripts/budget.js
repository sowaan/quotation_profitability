frappe.ui.form.on('Budget', {
    // onload(frm) {
    //     console.log("Budget onload");
    //     // 🛡️ Guard: run only once
    //     if (frm.__accounts_loaded) return;
    //     frm.__accounts_loaded = true;

    //     console.log("Budget onload12");

    //     const rows = frappe.route_options?.__budget_rows || [];
    //     console.log("rows: ", frappe.route_options);
    //     if (!rows.length) return;

    //     rows.forEach(row => {
    //         const child = frm.add_child("accounts");
    //         child.account = row.gl_account;
    //         child.budget_amount = row.cost_amount;
    //     });

    //     frm.refresh_field("accounts");

    //     // 🧹 cleanup (CRITICAL)
    //     delete frappe.route_options.__budget_rows;
    // },

    refresh(frm) {
        console.log("Budget refresh");
    }
});
