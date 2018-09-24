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
			d.module = $("#id_module").val();
			d.row = $("#id_row").val();
			d.section = $("#id_section").val();
			d.shelf = $("#id_shelf").val();
      	}
	},
	"columns": [
 	        { "data": "series", "width": "150px" },
			{ "data": "carrier_type", "width": "200px" },
			{ "data": "quantity", "width": "100px",  "sortable": false, "class": "action_column" },
            { "data": "mrss", "sortable": false, "class": "action_column" },
			{ "data": "size", "width": "100px",  "sortable": false, "class": "action_column" },
		    { "data": "action", "width": "100px", "sortable": false, "class": "action_column" }
    ],
	"fnDrawCallback": function( oSettings ) {
      $('[data-toggle="tooltip"]').tooltip();
    }
});

$('#id_fonds').on('change', function (evt) {
	table.ajax.reload();
});

$('#id_row').on('change', function (evt) {
	table.ajax.reload();
});

$('#id_module').on('change', function (evt) {
	table.ajax.reload();
});

$('#id_section').on('change', function (evt) {
	table.ajax.reload();
});

$('#id_shelf').on('change', function (evt) {
	table.ajax.reload();
});

$('#mlr_filter_fonds_select_reset').on('click', function(e) {
	e.preventDefault();
	$("#id_fonds").val([]).trigger('change');
	$('#id_module').val("").trigger('change');
	$('#id_section').val("").trigger('change');
	$('#id_row').val("").trigger('change');
	$('#id_shelf').val("").trigger('change');
	$('#mlr_csv_export').attr('href', '/mlr/exportcsv');
});

$('#mlr_csv_export').on('click', function(e) {
	var params = "/mlr/exportcsv?";

	if($("#id_fonds").val()) {
		params += "&fonds_id=" + $("#id_fonds").val();
	}

	if($("#id_module").val()) {
		params += "&module=" + $("#id_module").val();
	}

	if($("#id_row").val()) {
		params += "&row=" + $("#id_row").val();
	}

	if($("#id_section").val()) {
		params += "&section=" + $("#id_section").val();
	}

	if($("#id_shelf").val()) {
		params += "&shelf=" + $("#id_shelf").val();
	}

	$(this).attr("href", params);
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