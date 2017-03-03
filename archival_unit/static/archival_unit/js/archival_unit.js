/**
 *
 */
var table = $('#archival_unit_table').DataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
		   { "visible": false},
 	       { "width": "180px" },
           { "sortable": false},
           { "sortable": false},
           { "sortable": false, "class": "action_column"},
           { "sortable": false, "class": "action_column"},
 	 ],
});

var series_table = $('#archival_unit_series_table').DataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
		   { "visible": false},
 	       { "width": "180px" },
           { "sortable": false},
           { "sortable": false},
           { "sortable": false, "class": "action_column"},
 	 ],
});

$(function() {
	$.fm({
		modal_head_selector: '.modal-title',
		debug: false,
		custom_callbacks: {
            "reloadTable": function(data, options) {
				table.ajax.reload(null, false);
            },
			"reloadSeriesTable": function (data, options) {
				series_table.ajax.reload(null, false);
			}
        }
	});
});