$('select').on('change', function (evt) {
	$('#fa-container').attr('href', '/container/' + $("#id_archival_unit").val());
});