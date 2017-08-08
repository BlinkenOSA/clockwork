/**
 *
 */
var table = $('#language_table').DataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
			{ "data": "language" },
			{ "data": "iso_639_1" },
			{ "data": "iso_639_2" },
		   	{ "data": "action", "class": "action_column" }
 	]
});

function displayMessage(message) {
    new Noty({
        type: 'success',
        theme: 'bootstrap-v3',
        text: message,
        timeout: 1000,
        closeWith: ['click', 'button']
    }).show()
}

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