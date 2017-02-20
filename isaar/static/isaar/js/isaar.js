/**
 *
 */
$('#isaar_table').dataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
 	        { "width": "50px" },
			{ "sortable": false },
            { "sortable": false },
            { "sortable": false },
		    { "width": "100px", "sortable": false, "class": "action_column" },
    ]
});
