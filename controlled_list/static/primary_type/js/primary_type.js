/**
 *
 */
var table = $('#primary_type_table').DataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
			{ "data": "type"},
		   	{ "data": "action", "class": "action_column", "sortable": false, "width": "100px" }
 	],
	"fnDrawCallback": function( oSettings ) {
      $('[data-toggle="tooltip"]').tooltip();
    }
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