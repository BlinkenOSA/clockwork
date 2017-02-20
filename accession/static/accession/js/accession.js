/**
 *
 */
$('#accession_table').dataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
 	       { "width": "100px" },
 	       { "sortable": false },
		   {  },
		   { "width": "100px", "sortable": false, "class": "action_column" },
 	 ],
});