/**
 *
 */
var table = $('#country_table').DataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
			{ "data": "country"},
			{ "data": "authority_url", "sortable": false},
 	       	{ "data": "alpha2", "width": "60px" },
 	       	{ "data": "alpha3", "width": "60px" },
		   	{ "data": "action", "class": "action_column", "width": "100px", "sortable": false }
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