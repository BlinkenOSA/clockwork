/**
 *
 */
var table = $('#accession_table').dataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
 	       { "width": "100px" },
 	       { "sortable": false },
		   {  },
		   { "width": "100px", "sortable": false, "class": "action_column" }
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