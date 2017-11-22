getCarrierType();
getLinearMeter();
getPublishedItems();
getISAD();
getDuration();

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

var ctChart;

$('#id_fonds').on('change', function (evt) {
	subfonds.val(null).trigger("change");
});

$('#id_subfonds').on('change', function (evt) {
	series.val(null).trigger("change");
});

$('#id_series').on('change', function (evt) {
    getCarrierType();
    getLinearMeter();
    getPublishedItems();
    getISAD();
    getDuration();
});

function getArchivalUnit() {
    var archival_unit;
    if($('#id_fonds').val()) {
        archival_unit = $('#id_fonds').val();
    }
    if($('#id_subfonds').val()) {
        archival_unit = $('#id_subfonds').val();
    }
    if($('#id_series').val()) {
        archival_unit = $('#id_series').val();
    }
    return archival_unit;
}

function getCarrierType() {
    var au = (getArchivalUnit() === undefined) ? 0 : getArchivalUnit();
    $.ajax({
        url: "/dashboard/statistics/carrier_type/" + au,
        method: "GET",
        success: function (data) {
            if (ctChart) {
                ctChart.destroy();
            }

            var auCarriers = document.getElementById('archival-unit-carriers-chart').getContext('2d');

            ctChart = new Chart(auCarriers, {
                type: 'doughnut',
                data: data,
                options: {
                    title: {
                        display: true,
                        text: data.datasets[0].label
                    },
                }
            });
        },
        error: function (data) {
            console.log(data);
        }
    });
}

function getLinearMeter() {
    var au = (getArchivalUnit() === undefined) ? 0 : getArchivalUnit();
    $.ajax({
        url: "/dashboard/statistics/linear_meter/" + au,
        method: "GET",
        success: function (data) {
            $('#linear-meter-number').text(data['linear_meter']);
            $('#linear-meter-progress-bar').css('width', data['linear_meter_percentage'] + '%');
            $('#linear-meter-progress-description').text(data['linear_meter_message']);
        },
        error: function (data) {
            console.log(data);
        }
    });
}

function getPublishedItems() {
    var au = (getArchivalUnit() === undefined) ? 0 : getArchivalUnit();
    $.ajax({
        url: "/dashboard/statistics/published_items/" + au,
        method: "GET",
        success: function (data) {
            $('#published-items-number').text(data['published_items']);
            $('#published-items-progress-bar').css('width', data['published_items_percentage'] + '%');
            $('#published-items-progress-description').text(data['published_items_message']);
        },
        error: function (data) {
            console.log(data);
        }
    });
}

function getExtents() {
    var au = (getArchivalUnit() === undefined) ? 0 : getArchivalUnit();
    $.ajax({
        url: "/dashboard/statistics/extents/" + au,
        method: "GET",
        success: function (data) {
            $('#extents-number').text(data['extents']);
            $('#extents-progress-description').text(data['extents_message']);
        },
        error: function (data) {
            console.log(data);
        }
    });
}

function getISAD() {
    var au = (getArchivalUnit() === undefined) ? 0 : getArchivalUnit();
    $.ajax({
        url: "/dashboard/statistics/isad/" + au,
        method: "GET",
        success: function (data) {
            $('#isad-number').text(data['isad']);
            $('#isad-progress-bar').css('width', data['isad_percentage'] + '%');
            $('#isad-progress-description').text(data['isad_message']);
        },
        error: function (data) {
            console.log(data);
        }
    });
}

function getDuration() {
    var au = (getArchivalUnit() === undefined) ? 0 : getArchivalUnit();
    $.ajax({
        url: "/dashboard/statistics/duration/" + au,
        method: "GET",
        success: function (data) {
            $('#duration-number').text(data['duration']);
            $('#duration-progress-description').text(data['duration_message']);
        },
        error: function (data) {
            console.log(data);
        }
    });
}