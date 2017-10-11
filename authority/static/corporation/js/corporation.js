/**
 *
 */
var table = $('#corporation_table').DataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
			{ "data": "name"},
			{ "data": "authority_url", "sortable": false },
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