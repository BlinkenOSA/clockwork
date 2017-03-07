// DataTable Init
var table = $('#fa_table').DataTable({
    "dom": "lrtip",
	"serverSide": true,
	"ajax": "/finding_aids/datatable/" + containerID ,
	"columns": [
       { "data": 'level', "width": "5%", "class": "action_column" },
	   { "data": 'folder_no', "width": "5%", "class": "action_column" },
       { "data": 'item_no', "width": "5%", "class": "action_column" },
	   { "data": 'title', "width": "25%" },
	   { "data": 'title_original', "width": "30%" },
	   { "data": 'date', "width": "20%" },
       { "data": 'action', "width": "10%", "class": "action_column" },
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

$(function() {
	$.fm({
		modal_head_selector: '.modal-title',
		debug: false,
   		custom_callbacks: {
            "reloadTable": function (data, options) {
                table.ajax.reload(null, false);
            }
        }
	});
});

$(document).ready(function() {
	$("div.fm-modal").on('shown.bs.modal', function () {
		if(action == "create") {
		    $('#id_folder_no_select').attr('disabled', true)
			calculateFolderNumber();
		}
	});
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

