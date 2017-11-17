/**
 *
 */
var table = $('#donor_table').DataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
 	       { "data": 'name' },
 	       { "data": 'address', "sortable": false },
		   { "data": 'action', "sortable": false, "width": "100px", "class": "action_column" }
 	 ],
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