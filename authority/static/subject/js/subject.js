/**
 *
 */
var table = $('#subject_table').DataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
			{ "data": "subject" },
			{ "data": "authority_url", "sortable": false },
		   	{ "data": "action", width: "100px", "class": "action_column" }
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