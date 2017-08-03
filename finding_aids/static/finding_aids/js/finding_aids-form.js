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

changeflag();

$( "#id_original_locale" ).change(function() {
    changeflag();
});

$(document).on('change', '#id_folder_no_select', function() {
	$('#id_folder_no').val($('#id_folder_no_select').val());
	calculateItemNumber();
})

$(document).on('click', '#id_level_0', function() {
    $('#id_folder_no_select').attr('disabled', true)
    $('#id_item_no_select').attr('disabled', true);
	if(action == "create") {
		calculateFolderNumber();
	}
});

$(document).on('click', '#id_level_1', function() {
	if(action == "create") {
	    $('#id_folder_no_select').attr('disabled', false);
		calculateItemNumber();
	}
});

function calculateFolderNumber() {
	$('#id_folder_no_select').empty();
	$('#id_item_no_select').empty();

	$.ajax({
		url: "./statistics"
	}).done(function(data) {
		$.each(data["stats"], function(key, value) {
			 $('#id_folder_no_select').append($("<option></option>").attr("value",key).text(key));
		});
		$('#id_folder_no_select option').last().prop('selected',true);
		$('#id_item_no').val(0);
	});
}

function calculateItemNumber() {
	var folder_no = $('#id_folder_no_select').val();

	$.ajax({
		url: "./statistics"
	}).done(function(data) {
		$('#id_item_no').val(data['stats'][folder_no]+1);
	});
}

