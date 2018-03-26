// DataTable Init
var table = $('#fa_table').DataTable({
	"serverSide": true,
	"ajax": "/finding_aids/datatable/" + containerID ,
	"dom": "<'row'<'col-sm-3'l><'col-sm-3'<'opendisplay'>><'col-sm-6'f>>" +
		   "<'row'<'col-sm-12'tr>>" +
		   "<'row'<'col-sm-5'i><'col-sm-7'p>>",
	"columns": [
       	{ "data": 'level', "width": "20%", "class": "call_no_column"},
		{ "data": 'more_button', "className": 'details-control', "orderable": false, "defaultContent": '' },
	   	{ "data": 'title', "width": "40%" },
	   	{ "data": 'date', "width": "15%" },
       	{ "data": 'action', "width": "15%", "class": "action_column" },
		{ "data": 'publish', "width": "10%", "class": "action_column" },
	],
    "rowCallback": function( row, data, index ) {
      	if ( data.item_no != 0 ) {
	    	$(row).addClass('item');
			return row;
	  	}
	},
	"lengthMenu": [ [10, 25, 50, -1], [10, 25, 50, "All"] ],
	"paging":   true,
    "ordering": false,
    "info":     false,
	"searching": true,
	"autoWidth": true,
	"stateSave": true
});

$('div.opendisplay').html(
	'<div class="btn-group">' +
		'<a class="btn btn-default btn-sm details-show" href="#">Show Details</a>' +
		'<a class="btn btn-default btn-sm details-hide" href="#">Hide Details</a>' +
	'</div>'
);

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

$('tbody').on('click','.btn-clone',function(e) {
	e.preventDefault();
	$.ajax({
      type: 'POST',
	  success: function(data) {
		  table.ajax.reload(null, false);
	  },
      error: function(){ },
      url: $(this).attr("href"),
      cache: false
    });
});


$('tbody').on('click','.btn-confidential',function(e) {
	e.preventDefault();
	var url = $(this).attr("href");
	var msg = "Are you sure you want to 'Set/Unset Confidential' the Finding Aids record?";
	alertify.confirm(msg, function (e) {
		$.ajax({
			type: 'POST',
			success: function (data) {
				table.row('#' + data['DT_rowId']).data(data);
			},
			error: function () {
			},
			url: url,
			cache: false
		});
	});
});


$('tbody').on('click','.btn-action',function(e) {
	e.preventDefault();
	var url = $(this).attr("href");
	var msg = "Are you sure you want to 'Publish/Unpublish' the Finding Aids record?";
	alertify.confirm(msg, function (e) {
		$.ajax({
			type: 'POST',
			success: function (data) {
				table.row('#' + data['DT_rowId']).data(data);
			},
			error: function () {
			},
			url: url,
			cache: false
		});
	});
});

$('#publish_all').on('click', function(e) {
	e.preventDefault();
	var url = $(this).attr("href");
	var msg = "Are you sure you want to set all the Finding Aids entries 'Ready for publish'?";
	alertify.confirm(msg, function (e) {
		$.ajax({
			type: 'POST',
			success: function (data) {
				table.ajax.reload();
			},
			error: function () {
			},
			url: url,
			cache: false
		});
	});
});

$(function() {
	$.fm({
		modal_head_selector: '.modal-title',
		debug: false,
		custom_callbacks: {
            "reloadTable": function(data, options) {
                table.ajax.reload(null, false);
				displayMessage(data["message"]);
            }
        }
	});
});

function getDetails ( d ) {
	if (d.contents_summary) {
		return $('<tr>' +
					'<td></td>' +
					'<td></td>' +
					'<td colspan="3">' +
						'<div class="slider" style="display:none;">' +
							'<i>Contents Summary</i>' +
							'<p>'+d.contents_summary+'</p>' +
						'</div>' +
					'</td>' +
				'</tr>');
	} else {
		return undefined;
	}

}

$('#fa_table tbody').on('click', 'td.details-control', function () {
	var tr = $(this).closest('tr');
	var row = table.row( tr );

	if ( row.child.isShown() ) {
		// Close this row
		if (row.child()) {
			$('div.slider', row.child()).slideUp( function () {
				row.child.hide();
				tr.removeClass('shown');
			});
		}
		$(this).html('<i class="fa fa-plus-square-o"></i>')
	}
	else {
		// Open this row
		let content = getDetails(row.data());
		if (content) {
			row.child(content).show();
			tr.addClass('shown');
			$('div.slider', row.child()).slideDown();
		}
		$(this).html('<i class="fa fa-minus-square-o"></i>')
	}
});

$("a.details-show").on('click', function(e){
	e.preventDefault();
	table.rows().every( function () {
		let content = getDetails(this.data());
		if(content) {
			this.child(content).show();
			$('div.slider', this.child()).slideDown();
			table.cell(this, 1).data('<i class="fa fa-minus-square-o"></i>');
		}
	});
});

$("a.details-hide").on('click', function(e){
	e.preventDefault();
	table.rows().every( function () {
		let row = this;
		let child = this.child();
		if (child) {
			$('div.slider', child).slideUp( function () {
				child.hide();
				table.cell(row, 1).data('<i class="fa fa-plus-square-o"></i>');
			});
		}
	});
});