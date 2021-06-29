var table = $('#digitization_table').DataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
 	       { "data": 'container_no', "sortable": true },
 	       { "data": 'barcode', "sortable": true },
		   { "data": 'digital_version_exists', "sortable": true, "width": "100px", "class": "action_column"},
		   { "data": 'digital_version_creation_date', "sortable": true },
           { "data": 'duration', "sortable": false },
           { "data": 'carrier_type', "sortable": true },
		   { "data": 'action', "sortable": false, "width": "100px", "class": "action_column" }
 	],
	"fnDrawCallback": function( oSettings ) {
      $('[data-toggle="tooltip"]').tooltip();
	  $('.modal').on('hidden.bs.modal', function(e) {
    	$(this).removeData();
	  });
    }
});
