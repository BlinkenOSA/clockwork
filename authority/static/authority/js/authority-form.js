/**
 *
 */
function authorityTablesInit(authority_type) {
	var viaf_table = $('#viaf_table').DataTable({
		'paging'      : false,
		'lengthChange': false,
		'searching'   : false,
		'ordering'    : false,
		'info'        : false,
		'autoWidth'   : false,
		"serverSide": true,
		"ajax": "../viaf_datatable",
		"columns": [
				{ "data": "viaf_id" },
				{ "data": "name" },
				{ "data": "action", "class": "action_column" }
		]
	});

	var lcsh_table = $('#lcsh_table').DataTable({
		'paging'      : false,
		'lengthChange': false,
		'searching'   : false,
		'ordering'    : false,
		'info'        : false,
		'autoWidth'   : false,
		"serverSide": true,
		"ajax": "../lcsh_datatable",
		"columns": [
				{ "data": "lcsh_id" },
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

	function getQueryValue(authority_type) {
		switch(authority_type) {
			case 'person':
				return $('#id_first_name').val() + ' ' + $('#id_last_name').val();
			case 'corporation':
				return $('#id_name').val();
			case 'country':
				return $('#id_country').val();
			case 'genre':
				return $('#id_genre').val();
			case 'place':
				return $('#id_place').val();
			case 'subject':
				return $('#id_subject').val();
			default:
				return " "
		}
	}

	function stopVIAFButton() {
		$('#check_viaf').button('reset');

		$('a.select_viaf').click(function(e) {
			var trow = $(this).parents('tr');
			var d = viaf_table.row( trow ).data();
			var dhtml = $.parseHTML(d['viaf_id']);
			$('#id_authority_url').val(dhtml[0].text);
		});
	}

	$('#check_viaf').click(function(e) {
		e.preventDefault();
		var query = getQueryValue(authority_type);

		if(query != " ") {
			$(this).button('loading');
			viaf_table.ajax.url( '../viaf_datatable?q=' + query + '&auth_type=' + authority_type).load(stopVIAFButton, true);
		}
	});

	function stopLCSHButton() {
		$('#check_lcsh').button('reset');

		$('a.select_lcsh').click(function(e) {
			var trow = $(this).parents('tr');
			var d = lcsh_table.row( trow ).data();
			var dhtml = $.parseHTML(d['lcsh_id']);
			$('#id_authority_url').val(dhtml[0].text);
		});
	}

	$('#check_lcsh').click(function(e) {
		e.preventDefault();
		var query = getQueryValue(authority_type);

		if(query != " ") {
			$(this).button('loading');
			lcsh_table.ajax.url( '../lcsh_datatable?q=' + query + '&auth_type=' + authority_type).load(stopLCSHButton, true);
		}
	});


	function stopWikiButton() {
		$('#check_wiki').button('reset');

		$('a.select_wiki').click(function(e) {
			var trow = $(this).parents('tr');
			var d = wiki_table.row( trow ).data();
			var dhtml = $.parseHTML(d['wiki_url']);
			$('#id_wiki_url').val(dhtml[0].text);
		});
	}

	$('#check_wiki').click(function(e) {
		e.preventDefault();
		var query = getQueryValue(authority_type);

		if(query != " ") {
			$(this).button('loading');
			wiki_table.ajax.url( '../wikipedia_datatable?q=' + query).load(stopWikiButton, true);
		}
	});

}