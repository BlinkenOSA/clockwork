
subformCreate('creators');
subformCreate('extents');
subformCreate('carriers');
subformCreate('related_finding_aids');
subformCreate('location_of_originals');
subformCreate('location_of_copies');

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

infobox_call_and_update('isad', 'edit_page');
register_infobox('isad');