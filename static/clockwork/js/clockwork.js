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
    alertify.logPosition("bottom left");
	alertify.delay(5000).success(message);
}
// AdminLTE sidebar hack
$.AdminLTESidebarTweak = {};

$.AdminLTESidebarTweak.options = {
        EnableRemember: true,
        NoTransitionAfterReload: true
        //Removes the transition after page reload.
};

$(function () {
    "use strict";

    $("body").on("collapsed.pushMenu", function() {
        if($.AdminLTESidebarTweak.options.EnableRemember) {
            localStorage.setItem("toggleState", "closed");
        }
    });

    $("body").on("expanded.pushMenu", function() {
            if($.AdminLTESidebarTweak.options.EnableRemember) {
                localStorage.setItem("toggleState", "opened");
            }
    });

    if ($.AdminLTESidebarTweak.options.EnableRemember) {
        var toggleState = localStorage.getItem("toggleState");
        if (toggleState == 'closed'){
            if ($.AdminLTESidebarTweak.options.NoTransitionAfterReload) {
                $("body").addClass('sidebar-collapse hold-transition').delay(100).queue(function() {
                    $(this).removeClass('hold-transition');
                });
            } else {
                $("body").addClass('sidebar-collapse');
            }
        }
    }
});
