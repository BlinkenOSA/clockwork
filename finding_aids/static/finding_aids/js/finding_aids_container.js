// DataTable Init
var table = $('#fa_table').DataTable({
    "dom": "lrtip",
	"serverSide": true,
	"ajax": "/finding_aids/datatable/" + containerID ,
	"columns": [
       	{ "data": 'level', "width": "20%", "class": "call_no_column"},
	   	{ "data": 'title', "width": "40%" },
	   	{ "data": 'date', "width": "15%" },
       	{ "data": 'action', "width": "15%", "class": "action_column" },
		{ "data": 'publish', "width": "10%", "class": "action_column" },
	],
    "rowCallback": function( row, data, index ) {
      if ( data.item_no != 0 ) {
	    $(row).addClass('item');
		return row;
	  }
    },
	"lengthMenu": [ [10, 25, 50, -1], [10, 25, 50, "All"] ],
	"paging":   true,
    "ordering": false,
    "info":     false,
	"searching": false,
	"autoWidth": true,
	"stateSave": true
});

$(document).on('change', '#id_folder_no_select', function() {
	$('#id_folder_no').val($('#id_folder_no_select').val());
	calculateItemNumber();
})

$(document).on('click', '#id_level_0', function() {
    $('#id_folder_no_select').attr('disabled', true)
    $('#id_item_no_select').attr('disabled', true);
	if(action == "create") {
		calculateFolderNumber();
	}
});

$(document).on('click', '#id_level_1', function() {
	if(action == "create") {
	    $('#id_folder_no_select').attr('disabled', false);
		calculateItemNumber();
	}
});

function calculateFolderNumber() {
	$('#id_folder_no_select').empty();
	$('#id_item_no_select').empty();

	$.ajax({
		url: "./statistics"
	}).done(function(data) {
		$.each(data["stats"], function(key, value) {
			 $('#id_folder_no_select').append($("<option></option>").attr("value",key).text(key));
		});
		$('#id_folder_no_select option').last().prop('selected',true);
		$('#id_item_no').val(0);
	});
}

function calculateItemNumber() {
	var folder_no = $('#id_folder_no_select').val();

	$.ajax({
		url: "./statistics"
	}).done(function(data) {
		$('#id_item_no').val(data['stats'][folder_no]+1);
	});
}

$('tbody').on('click','.btn-clone',function(e) {
	e.preventDefault();
	$.ajax({
      type: 'POST',
	  success: function(data) {
		  table.ajax.reload(null, false);
	  },
      error: function(){ },
      url: $(this).attr("href"),
      cache: false
    });
});


$('tbody').on('click','.btn-action',function(e) {
	e.preventDefault();
	var url = $(this).attr("href");
	var msg = "Are you sure you want to 'Publish/Unpublish' the Finding Aids record?";
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
	var msg = "Are you sure you want to set all the Finding Aids entries 'Ready for publish'?";
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