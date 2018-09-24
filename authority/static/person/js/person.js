/**
 *
 */
var table = $('#person_table').DataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
			{ "data": "person_name" },
			{ "data": "authority_url", "sortable": false },
		   	{ "data": "action", "class": "action_column" }
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