



frappe.ui.form.on('Quotation', {

    custom_costing_rate_from_product_bundle: function(frm)
    {

        
        if (frm.doc.custom_costing_rate_from_product_bundle == 1)
        {
            if (frm.doc.items)
            {
               
                frm.doc.items.forEach( x => {
                    frappe.model.set_value(x.doctype , x.name , "custom_clearance_cost" , 0) ;
                    frappe.model.set_value(x.doctype , x.name , "custom_freight_charges_cost" , 0) ;
                    frappe.model.set_value(x.doctype , x.name , "custom_installation_charges_cost" , 0) ;
                    frappe.model.set_value(x.doctype , x.name , "custom_customs_cost" , 0) ;
                    // frappe.model.set_value(x.doctype , x.name , "custom_make_fields_read_only" , 1) ;
                    
                });
                frm.fields_dict["items"].grid.refresh() ;
            }
        }

        else
        {
            if (frm.doc.items)
                {
                    frm.doc.items.forEach( x => {
                        frappe.model.set_value(x.doctype , x.name , "custom_make_fields_read_only" , 0) ;       
                    });
                    frm.fields_dict["items"].grid.refresh() ;
                }
        }



    },


});
