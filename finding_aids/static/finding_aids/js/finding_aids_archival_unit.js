var fonds = $('#id_fonds').djangoSelect2({
	placeholder: '- Select Fonds -',
	escapeMarkup: function (m) { return m; }
});

var subfonds = $('#id_subfonds').djangoSelect2({
	placeholder: '- Select Subfonds -',
	escapeMarkup: function (m) { return m; }
});

var series = $('#id_series').djangoSelect2({
	placeholder: '- Select Series -',
	escapeMarkup: function (m) { return m; }
});

$('#id_fonds').on('change', function (evt) {
	subfonds.val(null).trigger("change");
});

$('#id_subfonds').on('change', function (evt) {
	series.val(null).trigger("change");
});

$('#id_series').on('change', function (evt) {
	if($("#id_series").val()) {
		$('#fa-container').attr('href', '/container/' + $("#id_series").val());
	} else {
		$('#fa-container').attr('href', '/container/#');
	}
});

$('#fa-container').on('click', function(e) {
	if (!($("#id_series").val())) {
		e.preventDefault();
	}
});
