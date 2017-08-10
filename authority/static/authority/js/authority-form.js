/**
 *
 */
function authorityTablesInit() {

	var authority_table = $('#authority_table').DataTable({
		'paging'      : false,
		'lengthChange': false,
		'searching'   : false,
		'ordering'    : false,
		'info'        : false,
		'autoWidth'   : false,
		"serverSide": true,
		"ajax": "../authority_datatable",
		"columns": [
				{ "data": "viaf_id" },
				{ "data": "name" },
				{ "data": "action", "class": "action_column" }
		]
	});

	var wiki_table = $('#wiki_table').DataTable({
		'paging'      : false,
		'lengthChange': false,
		'searching'   : false,
		'ordering'    : false,
		'info'        : false,
		'autoWidth'   : false,
		"serverSide": true,
		"ajax": "../wikipedia_datatable",
		"columns": [
				{ "data": "wiki_url" },
				{ "data": "name" },
				{ "data": "action", "class": "action_column" }
		]
	});

	function updateVIAFCounter() {
		var tabText = 'Authority Check (' + authority_table.rows().count() + ')';
		$('#authority_check_tab').text(tabText);
		$('#check_viaf').button('reset');
	}

	$('#check_viaf').click(function(e) {
		$(this).button('loading');
		e.preventDefault();
		var query = $('#id_first_name').val() + ' ' + $('#id_last_name').val()
		if(query.length > 0) {
			authority_table.ajax.url( '../authority_datatable?q=' + query + '&auth_type=person').load(updateVIAFCounter, true);
		}
	});
}