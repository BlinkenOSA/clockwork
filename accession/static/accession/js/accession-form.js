subformCreate('accession_items');

$(function() {
	$.fm({
		modal_head_selector: '.modal-title',
		debug: false,
		custom_callbacks: {
            "selectDonor": function(data) {
                var s2 = $('[name="donor"]').data('select2');
                s2.trigger('select', {
                    data: {"id": data.entry_id, "text": data.entry_name }
                });
            }
        }
	});
});

