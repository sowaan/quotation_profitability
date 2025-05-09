











frappe.ui.form.on('Material Request', {
        refresh(frm) {

            if (frm.doc.docstatus == 0)
            {

                frm.add_custom_button('BOQ Bundle Items', () => {
                    let dialog = new frappe.ui.Dialog({
                        title: 'BOQ Packed Items',
                        fields: [
                            {
                                label: 'BOQ',
                                fieldname: 'boq',
                                fieldtype: 'Link',
                                options: 'Quotation',
                                reqd: 1,
                                get_query: () => {
                                    return {
                                        filters: { docstatus: 1 } // only submitted
                                    };
                                },
                                onchange: async function () {
                                    const boq_name = dialog.get_value('boq');
                                    if (!boq_name) return;
        
                                    // Show loading
                                    dialog.set_df_property('items_table', 'hidden', true);
                                    dialog.set_df_property('items_table', 'data', []);
                                    
                                    try {
                                        const boq_doc = await frappe.db.get_doc('Quotation', boq_name);
                                        
                                        // Prepare items data
                                        const items = boq_doc.packed_items.map(item => {
                                            return {
                                                item_code: item.item_code,
                                                item_name: item.item_name,
                                                qty: item.qty,
                                                uom: item.uom
                                            };
                                        });
                                        
                                        // Set table data
                                        dialog.set_df_property('items_table', 'data', items);
                                        dialog.set_df_property('items_table', 'hidden', false);
                                    } catch (error) {
                                        frappe.msgprint(__('Error loading BOQ items: ') + error.message);
                                    }
                                }
                            },
                            {
                                fieldname: 'items_table',
                                fieldtype: 'Table',
                                label: 'Items',
                                hidden: true,
                                in_place_edit: true,
                                data: [],
                                fields: [
                                    {
                                        fieldtype: 'Link',
                                        fieldname: 'item_code',
                                        label: __('Item Code'),
                                        options: 'Item',
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                    {
                                        fieldtype: 'Data',
                                        fieldname: 'item_name',
                                        label: __('Item Name'),
                                        in_list_view: 1,
                                        read_only: 1
                                    },
                                    {
                                        fieldtype: 'Float',
                                        fieldname: 'qty',
                                        label: __('Qty'),
                                        in_list_view: 1,
                                        read_only: 0
                                    },
                                    {
                                        fieldtype: 'Link',
                                        fieldname: 'uom',
                                        label: __('UOM'),
                                        options: 'UOM',
                                        in_list_view: 1,
                                        read_only: 1
                                    }
                                ]
                            }
                        ],
                        size: 'large',
                        primary_action_label: 'Insert',
                        primary_action(values) {
                            // frappe.msgprint(`Selected BOQ: ${values.boq}`);
                            // const items_table = dialog.fields_dict.items_table;
                            // const items_data = items_table.get_data();
                            
                            // const selected_items = items_data.filter(item => item.select);
                            let selected_items = values.items_table.filter(row => row.__checked === 1);
                            
                            if (selected_items.length === 0) {
                                    frappe.msgprint(__('Please select at least one item'));
                                    return;
                            }
                            
                            // Add items to Material Request
                            selected_items.forEach(item => {
                                    const row = frm.add_child('items');
                                    frappe.model.set_value(row.doctype, row.name, {
                                    item_code: item.item_code,
                                    item_name: item.item_name,
                                    qty: item.qty,
                                    uom: item.uom
                                    });
                            });
                            
                            frm.refresh_field('items');
                            dialog.hide();
                        }
                        
                    });
        
                    dialog.show();
                });

            }
        }
    });












