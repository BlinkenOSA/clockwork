// DataTable Init
var table = $('#fa_template_table').DataTable({
    "dom": "lrtip",
	"serverSide": true,
	"ajax": "/finding_aids/templates/datatable/" + seriesID ,
	"columns": [
	   { "data": 'template_name', "width": "40%" },
	   { "data": 'user_created', "width": "40%" },
       { "data": 'action', "width": "20%", "class": "action_column" },
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
            "reloadTable": function(data, options) {
                table.ajax.reload(null, false);
				displayMessage(data["message"]);
            }
        }
	});
});