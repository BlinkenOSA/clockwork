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

infobox_call_and_update('donor', 'list_page');