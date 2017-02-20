/**
 *
 */
$('#donor_table').dataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
 	       { "width": "60px" },
 	       null,
 	       null,
		   { "width": "100px", "class": "action_column" },
 	 ],
});