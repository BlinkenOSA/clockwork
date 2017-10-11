// DataTable Init
var table = $('#container_table').DataTable({
    "dom": "lrtip",
	"serverSide": true,
	"ajax": "/container/datatable/" + archival_unit_id,
	"select": true,
	"columns": [
	   { "data": 'container_no', "width": "20%" } ,
	   { "data": 'identifier', "width": "20%" },
	   { "data": 'carrier_type', "width": "15%" },
	   { "data": 'primary_type', "width": "15%" },
	   { "data": 'action', "width": "10%", "class": "action_column" },
	   { "data": 'navigate', "width": "10%", "class": "action_column" },
	   { "data": 'publish', "width": "10%", "class": "action_column" }
	],
	"lengthMenu": [ [10, 25, 50, -1], [10, 25, 50, "All"] ],
	"paging":    true,
    "ordering":  false,
    "info":      false,
	"searching": false,
	"autoWidth": true,
    "stateSave": true
});


/* Create Container */
$('#container-create').on('click', function(e) {
	e.preventDefault();

	var primary_type = $('#id_primary_type').val();
	var carrier_type = $('#id_carrier_type').val();
	var container_label = $('#id_container_label').val();

	if (primary_type != "" && carrier_type != "") {
		var data = {
			'archival_unit': archival_unit_id,
			'primary_type': primary_type,
			'carrier_type': carrier_type,
			'container_label': container_label
		};

		$.ajax({
			type: 'POST',
			success: function(data) {
				table.page('last').draw(false);
			},
			error: function(){ },
			url: '/container/create/',
			data: data,
			cache: false
		});
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

$('tbody').on('click','.btn-action',function(e) {
	e.preventDefault();
	var url = $(this).attr("href");
	var msg = "Are you sure you want to 'Publish/Unpublish' all the Finding Aids records in the seleced Container?";
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

$('#publish_all').on('click', function(e) {
	e.preventDefault();
	var url = $(this).attr("href");
	var msg = "Are you sure you want to set all the Containers and the Finding Aids entries under them as 'Ready for publish'?";
	alertify.confirm(msg, function (e) {
		$.ajax({
			type: 'POST',
			success: function (data) {
				table.ajax.reload();
			},
			error: function () {
			},
			url: url,
			cache: false
		});
	});
});
