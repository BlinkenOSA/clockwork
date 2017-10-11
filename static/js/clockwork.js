$(".toggle-expand-btn").click(function (e) {
    $(this).closest('.box').toggleClass('panel-fullscreen');
});

function register_infobox(module) {
    $("input").on("click", function() {
        var form_field = ($(this).attr("name"));
        infobox_call_and_update(module, form_field)
    });

    $("textarea").on("click", function() {
        var form_field = ($(this).attr("name"));
        infobox_call_and_update(module, form_field)
    });

    $("select").on("click", function() {
        var form_field = ($(this).attr("name"));
        infobox_call_and_update(module, form_field)
    });
}

function infobox_call_and_update(module, form_field) {
    $.ajax({
        url: "/dashboard/infobox/" + module + "/" + form_field
    }).done(function( data ) {
        $('.info-text-header').html(data['title'])
        $('.info-text-wrapper p').html(data['text'])
    });
}

$('.modal').on('hidden.bs.modal', function(e) {
    $(this).removeData();
});

function displayMessage(message) {
	alertify.logPosition("top right");
	alertify.delay(5000).success(message);
}
