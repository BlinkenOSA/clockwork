/**
 *
 */
var table = $('#isad_table').DataTable({
	"serverSide": true,
	"ajax": "datatable",
	"columns": [
 	       { "data": 'reference_code', "width": "100px" },
           { "data": 'title' },
		   { "data": 'view-edit-delete', "width": "100px", "class": "action_column", "sortable": false },
		   { "data": 'action', "width": "100px", "class": "action_column", "sortable": false },
 	 ]
});

$('select').on('change', function (evt) {
	$('#isad-create').attr('href', 'create/' + $("#id_archival_unit").val());
});

$('tbody').on('click','.btn-action',function(e) {
	e.preventDefault();
	$.ajax({
      type: 'POST',
	  success: function(data) {
		  var table = $('#isad_table').DataTable();
		  table.row(data['id']).data(data);
	  },
      error: function(){ },
      url: $(this).attr("href"),
      cache: false
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