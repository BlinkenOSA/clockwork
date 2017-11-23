/**
 *
 */
var table = $('#carrier_type_table').DataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
			{ "data": "type"},
			{ "data": "width", "class": "action_column", "sortable": false, "width": "50px"},
			{ "data": "height", "class": "action_column", "sortable": false, "width": "50px"},
			{ "data": "depth", "class": "action_column", "sortable": false, "width": "50px"},
		   	{ "data": "action", "class": "action_column", "sortable": false, "width": "100px" }
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