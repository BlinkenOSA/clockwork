/**
 *
 */
var table = $('#language_table').DataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
			{ "data": "language", "width": "40%" },
			{ "data": "authority_url", "sortable": false, "width": "20%" },
			{ "data": "iso_639_1", "width": "10%"},
			{ "data": "iso_639_2", "width": "10%" },
		   	{ "data": "action", "width": "20%", "class": "action_column", "sortable": false }
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