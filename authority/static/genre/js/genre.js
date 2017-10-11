/**
 *
 */
var table = $('#genre_table').DataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
			{ "data": "genre", "width": "30%" },
			{ "data": "authority_url", "sortable": false },
		   	{ "data": "action", width: "100px", "class": "action_column", "sortable": false }
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