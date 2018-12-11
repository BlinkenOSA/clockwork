var container = document.getElementById('faTableView');
var data = [];

requiredValidator = function(value, callback) {
    if (value.length === 0) {
        callback(false);
    } else {
        callback(true);
    }
};

dummyValidator = function(value, callback) {
    callback(true)
};

function validateDate(value) {
    let chunks = [];
    let valid = false;

    switch (value.length) {
        case 0:
            return true;
            break;
        case 4:
            valid = !!isValidDate(1, 1, value);
            return valid;
            break;
        case 7:
            chunks = value.split("-");
            if(chunks.length === 2) {
                const year = chunks[0];
                const month = chunks[1];
                valid = !!isValidDate(1, month, year);
            }
            return valid;
            break;
        case 10:
            chunks = value.split("-");
            if(chunks.length === 3) {
                const year = chunks[0];
                const month = chunks[1];
                const day = chunks[2];
                valid = !!isValidDate(day, month, year);
            }
            return valid;
            break;
        default:
            return false;
    }
}

dateFromValidator = function(value, callback) {
    let valid, dateFrom, dateTo;
    dateTo = hot.getDataAtCell(this.row, 7);
    valid = validateDate(value);
    if(validateDate(value) && validateDate(dateTo)) {
        if(dateTo.length > 0) {
            dateFrom = new Date(value);
            dateTo = new Date(dateTo);
            valid = dateFrom < dateTo;
        } else {
            valid = true;
        }
    }
    callback(valid);
};

dateToValidator = function(value, callback) {
    let valid, dateFrom, dateTo;
    dateFrom = hot.getDataAtCell(this.row, 6);
    valid = validateDate(value);
    if(validateDate(value) && validateDate(dateFrom)) {
        if(value.length > 0) {
            dateFrom = new Date(dateFrom);
            dateTo = new Date(value);
            valid = dateFrom < dateTo;
        } else {
            valid = true;
        }
    }
    callback(valid);
};

function validateTime(value) {
    const timeFormat = /^(?:[01]\d|2[0123]):(?:[012345]\d):(?:[012345]\d)$/;

    if(value != "") {
        const match = value.match(timeFormat);
        return !!match;
    } else {
        return true;
    }
}

timeFromValidator = function(value, callback) {
    let valid, timeFrom, timeTo;
    valid = validateTime(value);
    timeFrom = value;
    timeTo = hot.getDataAtCell(this.row, 9) || '';
    if (timeTo.length > 0) {
        if (timeFrom > timeTo) {
            valid = false;
        }
    }
    callback(valid);
};

timeToValidator = function(value, callback) {
    let valid, timeFrom, timeTo;
    valid = validateTime(value);
    timeFrom = hot.getDataAtCell(this.row, 8) || '';
    timeTo = value;
    if(timeFrom.length === 0) {
        if(timeTo.length !== 0) {
            valid = false;
        }
    } else {
        if(timeTo.length !== 0) {
            if(timeFrom > timeTo) {
                valid = false;
            }
        }
    }
    callback(valid);
};

localeValidator = function(value, callback) {
    let valid = true;
    const title = hot.getDataAtCell(this.row, 2) || '';
    const contents_summary = hot.getDataAtCell(this.row, 5) || '';
    const note = hot.getDataAtCell(this.row, 12) || '';

    if(title.length > 0 || contents_summary.length > 0 || note.length > 0) {
        if(value.length === 0) {
            valid = false;
        }
    }
    callback(valid);
};

var columns = [
    {
        data: 'archival_reference_code',
        label: 'Archival Reference Code',
        editor: false
    }, {
        data: 'title',
        label: 'Title',
        width: 200,
        validator: requiredValidator,
        allowInvalid: true
    }, {
        data: 'title_original',
        label: 'Title (Original)',
        width: 200,
        validator: dummyValidator
    }, {
        data: 'original_locale',
        label: 'Locale',
        width: 100,
        type: 'dropdown',
        validator: localeValidator,
        source: ['Hungarian', 'Polish', 'Russian']
    }, {
        data: 'contents_summary',
        label: 'Contents Summary',
        width: 700,
        validator: dummyValidator
    }, {
        data: 'contents_summary_original',
        label: 'Contents Summary (Original)',
        width: 700,
        validator: dummyValidator
    }, {
        data: 'date_from',
        label: 'Date (from)',
        width: 100,
        validator: dateFromValidator,
        allowInvalid: true
    }, {
        data: 'date_to',
        label: 'Date (to)',
        width: 100,
        validator: dateToValidator,
        allowInvalid: true
    }, {
        data: 'time_start',
        label: 'Start time',
        width: 100,
        validator: timeFromValidator,
        allowInvalid: true
    }, {
        data: 'time_end',
        label: 'End time',
        width: 100,
        validator: timeToValidator,
        allowInvalid: true
    }, {
        data: 'duration',
        label: 'Duration',
        width: 100,
        editor: false
    }, {
        data: 'note',
        label: 'Note',
        width: 300
    }, {
        data: 'note_original',
        label: 'Note (Original)',
        width: 300
    }
];

var colHeaders = [];
columns.forEach(function(column) {
    colHeaders.push(column['label']);
});

var dataSchema = {};
columns.forEach(function(column) {
    dataSchema[column['data']] = null;
});

var options = {
    data: data,
    height: 600,
    colHeaders: colHeaders,
    dataSchema: dataSchema,
    columns: columns,
    rowHeaders: true,
    dropdownMenu: true,
    manualRowResize: true,
    manualColumnResize: true,
    viewportRowRenderingOffset: 10,
    undo: true,
    selectionMode: 'single',
    allowInvalid: false,
    autoRowSize: true,
    search: true
};

var hot = new Handsontable(container, options);

const maxData = 100;
var lastRowIdx = 100;
fetchData(maxData.toString());

function fetchData(limit, offset=0) {
    fetch(`/api/finding_aids/list/${selectedSeries}/?limit=${limit}&offset=${offset}`).then(function(response) {
        return response.json();
    }).then(function(data) {
        // let hotData = hot.getSourceData();
        // hot.loadData(hotData.concat(data.results));
        hot.loadData(data);
    });
}

hot.addHook("afterValidate", function(isValid, value, row, prop, source) {
    if(isValid) {
        const allowedActions = ['edit', 'UndoRedo.undo', 'UndoRedo.redo'];
        if(allowedActions.includes(source)) {
            let modifyData = {};
            modifyData[prop] = value;
            const r = hot.getSourceDataAtRow(row);
            const id = r['id'];
            fetch(`/api/finding_aids/${id}/`, {
                method: 'PATCH',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(modifyData)
            });
        }
    }
});

/*
hot.addHook("afterScrollVertically", function() {
    const lastCell = hot.getCell(lastRowIdx - 1, 1, true);
    const offset = lastRowIdx / maxData;
    if(lastCell && lastCell !== undefined) {
        fetchData(maxData.toString(), offset * maxData);
        lastRowIdx += maxData;
    }
});
*/

hot.addHook("afterChange", function(changes, source){
    if(changes) {
        changes.forEach(([row, prop, oldValue, newValue]) => {
            if(prop == 'time_start' || prop == 'time_end') {
                const timeFrom = hot.getDataAtCell(row, 8) || '';
                const timeTo = hot.getDataAtCell(row, 9) || '';
                const tf = moment(timeFrom, "hh:mm:ss");
                const tt = moment(timeTo, "hh:mm:ss");
                let updateValue = "";
                if(timeFrom.length > 0 && timeTo.length > 0 && timeFrom < timeTo && validateTime(timeFrom) && validateTime(timeTo)) {
                    updateValue = moment.utc(tt-tf).format("HH:mm:ss");
                } else {
                    updateValue = "";
                }
                hot.setDataAtCell(row, 10, updateValue, 'calc');
                const r = hot.getSourceDataAtRow(row);
                const id = r['id'];
                fetch(`/api/finding_aids/${id}/`, {
                    method: 'PATCH',
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({duration: updateValue})
                });
            }
        });
    }
});


$(".toggle-expand-btn").click(function (e) {
    const height = $(this).closest('.box').height() - 200;
    hot.updateSettings({
        height: height
    });
    hot.render();
});

const daysInMonth = function (m, y) {
    switch (m) {
        case 1 :
            return (y % 4 == 0 && y % 100) || y % 400 == 0 ? 29 : 28;
        case 8 : case 3 : case 5 : case 10 :
            return 30;
        default :
            return 31
    }
};

const isValidDate = function (d, m, y) {
    m = parseInt(m, 10) - 1;
    return m >= 0 && m < 12 && d > 0 && d <= daysInMonth(m, y);
};

function time_diff(t1, t2) {
   var parts = t1.split(':');
   var d1 = new Date(0, 0, 0, parts[0], parts[1], parts[2]);
   parts = t2.split(':');
   var d2 = new Date(new Date(0, 0, 0, parts[0], parts[1], parts[2]) - d1);
   // this would also work
   // d2.toTimeString().substr(0, d2.toTimeString().indexOf(' '));
   return (d2.getHours() + ':' + d2.getMinutes() + ':' + d2.getSeconds());
}