/**
 *
 */
var isadLevelFilter = "F";

var table = $('#isad_table').DataTable({
	"serverSide": true,
	"ajax": {
		"url": "datatable",
		"type": "GET",
      	"data": function(d){
			d.fonds = $("#id_fonds").val();
         	d.level = isadLevelFilter;
      	}
	},
	"columns": [
 	       { "data": 'reference_code', "width": "150px" },
           { "data": 'title' },
		   { "data": 'view-edit-delete', "width": "100px", "class": "action_column", "sortable": false },
		   { "data": 'status', "width": "100px", "class": "action_column", "sortable": true },
		   { "data": 'action', "width": "100px", "class": "action_column", "sortable": false }
 	 ]
 });

$('#id_archival_unit').on('change', function (evt) {
	$('#isad-create').attr('href', 'create/' + $("#id_archival_unit").val());
});

$('#id_fonds').on('change', function (evt) {
	table.ajax.reload();
});

$('#isad_filter_fonds_select_reset').on('click', function(e) {
	e.preventDefault();
	$("#id_fonds").val([]).trigger('change');
});

$('#isad_filter_fonds').on('click', function(e) {
	e.preventDefault();
	isadLevelFilter = "F";
	table.ajax.reload();
	$('.isad_filter_button').removeClass('active');
	$(this).addClass('active');
})

$('#isad_filter_subfonds').on('click', function(e) {
	e.preventDefault();
	isadLevelFilter = "SF";
	table.ajax.reload();
	$('.isad_filter_button').removeClass('active');
	$(this).addClass('active');
})

$('#isad_filter_series').on('click', function(e) {
	e.preventDefault();
	isadLevelFilter = "S";
	table.ajax.reload();
	$('.isad_filter_button').removeClass('active');
	$(this).addClass('active');
})

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

$('tbody').on('click','.btn-action',function(e) {
	e.preventDefault();
	var url = $(this).attr("href");
	var msg = "Are you sure you want to 'Publish/Unpublish' the ISAD(G) record?";
	alertify.confirm(msg, function (e) {
		$.ajax({
			type: 'POST',
			success: function (data) {
				table.row('#' + data['DT_rowId']).data(data);
			},
			error: function () {
			},
			url: url,
			cache: false
		});
	});
});