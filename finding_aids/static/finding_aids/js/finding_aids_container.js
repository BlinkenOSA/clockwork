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

$(document).on('click', '#id_level_0', function() {
    $('#id_item_no').attr('disabled', true);
})

$(document).on('click', '#id_level_1', function() {
    $('#id_item_no').attr('disabled', false);
})