var updateField = "";

function changeflag() {
    var flag = $('#id_original_locale').val().toLowerCase();
    if (flag) {
        var element = $('span.flag');
        element.removeClass();
        element.addClass('flag flag-' + flag);
        element.show();
    } else {
        $('span.flag').hide();
    }
}

$( "#id_original_locale" ).change(function() {
    changeflag();
});

$('.fm-create').on('click', function() {
	var ig = $(this).parents('div.input-group');
	updateField = ig.find('.django-select2').attr('name');
})

$('.django-select2').djangoSelect2();

subformCreate('languages');
subformCreate('extents');
subformCreate('dates');
subformCreate('associated_people');
subformCreate('associated_corporations');
subformCreate('associated_countries');
subformCreate('associated_places');

$(function() {
	$.fm({
		modal_head_selector: '.modal-title',
		debug: false,
		custom_callbacks: {
            "selectField": function(data) {
                var s2 = $('[name="'+updateField+'"]').data('select2');
				s2.trigger('select', {
                    data: {"id": data.entry_id, "text": data.entry_name }
                });
            }
        }
	});
});

/* TEMP */

$('#id_description_level').on('change', function() {
	var selection = ($('#id_description_level').val());
	switch(selection) {
		case 'L1':
			calculateFolderNumber();
			$("#id_level").prepend("<option value='F'>Folder</option>");
			$('#id_level').val('F');
			// $('#id_folder_no').prop('readonly', true);
			break;
		case 'L2':
			calculateItemNumber();
			$('#id_level').val('I');
			$("#id_level option[value='F']").remove();
			// $('#id_folder_no').prop('readonly', false);
			break;
	}
});

$('#id_folder_no').on('change', function() {
	calculateItemNumber();
});

function calculateFolderNumber() {
	$.ajax({
		url: "../get_new_folder"
	}).done(function(data) {
		$('#id_folder_no').val(data["stats"]["new_folder"]);
		$('#id_archival_reference_code').val(data["stats"]["new_arc"]);
	});
}

function calculateItemNumber() {
	$.ajax({
		url: "../get_new_item/" + $('#id_folder_no').val()
	}).done(function(data) {
		$('#id_archival_reference_code').val(data["stats"]["new_arc"]);
	});
}