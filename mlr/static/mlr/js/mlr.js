/**
 *
 */
var table = $('#mlr_table').DataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
 	        { "data": "series", "width": "150px" },
			{ "data": "carrier_type", "width": "100px", "sortable": false },
            { "data": "building", "sortable": false },
            { "data": "module", "sortable": false },
			{ "data": "row", "sortable": false },
			{ "data": "section", "sortable": false },
			{ "data": "shelf", "sortable": false },
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