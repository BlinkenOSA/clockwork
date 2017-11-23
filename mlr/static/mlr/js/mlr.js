/**
 *
 */
var table = $('#mlr_table').DataTable({
	"serverSide": true,
	"ajax": {
		"url": "datatable",
		"type": "GET",
		"data": function(d){
			d.fonds = $("#id_fonds").val();
      	}
	},
	"columns": [
 	        { "data": "series", "width": "150px" },
			{ "data": "carrier_type", "width": "200px" },
            { "data": "building", "sortable": false },
            { "data": "mrss", "sortable": false, "class": "action_column" },
		    { "data": "action", "width": "100px", "sortable": false, "class": "action_column" }
    ]
});

$('#id_fonds').on('change', function (evt) {
	table.ajax.reload();
	$('#mlr_csv_export').attr('href', '/mlr/exportcsv?fonds_id=' + $(this).val());
});

$('#mlr_filter_fonds_select_reset').on('click', function(e) {
	e.preventDefault();
	$("#id_fonds").val([]).trigger('change');
	$('#mlr_csv_export').attr('href', '/mlr/exportcsv');
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