/**
 *
 */
var table = $('#mlr_table').DataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
 	        { "data": "series", "width": "150px" },
			{ "data": "carrier_type", "width": "200px", "sortable": false },
            { "data": "building", "sortable": false },
            { "data": "mrss", "sortable": false },
		    { "data": "action", "width": "100px", "sortable": false, "class": "action_column" }
    ],
});

$("#mlr_table").find("tfoot th").each( function ( i ) {
	var select = $('<select><option value=""></option></select>')
		.appendTo( $(this).empty() )
		.on( 'change', function () {
			var val = $(this).val();

			table.column( i )
				.search( val ? '^'+$(this).val()+'$' : val, true, false )
				.draw();
		} );

	table.column( i ).data().unique().sort().each( function ( d, j ) {
		select.append( '<option value="'+d+'">'+d+'</option>' );
	} );
} );

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