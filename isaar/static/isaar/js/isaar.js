/**
 *
 */
var table = $('#isaar_table').dataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
 	        { "data": "id", "width": "50px" },
			{ "data": "name", "sortable": false },
            { "data": "type", "sortable": false },
            { "data": "status", "sortable": false },
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
