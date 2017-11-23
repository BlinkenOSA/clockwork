/**
 *
 */
var table = $('#isaar_table').dataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
			{ "data": "name", "sortable": true },
            { "data": "type", "sortable": false },
			{ "data": "isad", "sortable": false },
            { "data": "status", "sortable": false, "class": "action_column" },
		    { "data": "action", "width": "100px", "sortable": false, "class": "action_column" }
    ]
});

$(function() {
	$.fm({
		modal_head_selector: '.modal-title',
		debug: false,
		custom_callbacks: {
            "reloadTable": function(data, options) {
				table.ajax.reload(null, false);
                displayMessage(data["message"]);
            }
        }
	});
});

infobox_call_and_update('isaar', 'list_page');
