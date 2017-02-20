var editor = new $.fn.dataTable.Editor( {
	dom: "B",
	ajax: "/container/editor_update/",
	table: "#container_table",
	fields: [
		{
			label: "Container Number",
			name: "container_no",
			type: "readonly"
		}, {
			label: "Carrier Type ID",
			name: "carrier_type_identifier",
			type: "hidden"
		}, {
			label: "Carrier Type",
			name: "carrier_type",
			type: "select"
		}, {
			label: "Primary Type",
			name: "primary_type",
			type: "select"
		}, {
			label: "Primary Type ID",
			name: "primary_type_identifier",
			type: "hidden"
		}, {
            label: "Container",
            name: "container_label"
        }
	]
});

// DataTable Init
var table = $('#container_table').DataTable({
    "dom": "Blrtip",
	"serverSide": true,
	"ajax": "/container/datatable/" + archival_unit_id,
	"select": true,
	"columns": [
	   { "data": 'container_no', "width": "10%", "class": "action_column reorder" },
	   { "data": 'carrier_type_identifier', "visible": false },
	   { "data": 'carrier_type', "width": "30%" },
	   { "data": 'primary_type_identifier', "visible": false },
	   { "data": 'primary_type', "width": "30%" },
	   { "data": 'number_of_fa_entities', "width": "10%" },
	   { "data": 'container_label', "width": "20%" },
	   { "data": 'action', "width": "10%", "class": "action_column" }
	],
	"buttons": [
		{
			"extend": "edit",
			"editor": editor,
			formButtons: [
				{ label: 'Close', fn: function () { this.close(); }, className: "pull-left" },
				{ label: 'Save', fn: function () { this.submit(); }, className: 'btn-editor btn-primary'}
			],
			"text": '<i class="fa fa-edit"></i> Edit',
			"className": 'btn-default'
		}, {
			"extend": "remove",
			"editor": editor,
			formButtons: [
				{ label: 'Close', fn: function () { this.close(); }, className: "pull-left" },
				{ label: 'Delete', fn: function () { this.submit(); }, className: 'btn-editor btn-danger'}
			],
			"text": '<i class="fa fa-trash-o"></i> Delete',
			className: 'btn-default'
		}
	],
	"rowReorder": {
		"dataSrc": 'container_no',
        "editor":  editor,
		"update": false
    },
	"lengthMenu": [ [10, 25, 50, -1], [10, 25, 50, "All"] ],
	"paging":   true,
    "ordering": false,
    "info":     false,
	"searching": false,
	"autoWidth": true,
    "stateSave": true
});

/* Create Container */
$('#container-create').on('click', function(e) {
	e.preventDefault();

	var primary_type = $('#id_primary_type').val();
	var carrier_type = $('#id_carrier_type').val();
	var container_label = $('#id_container_label').val();

	if (primary_type != "" && carrier_type != "") {
		var data = {
			'archival_unit': archival_unit_id,
			'primary_type': primary_type,
			'carrier_type': carrier_type,
			'container_label': container_label
		};

		$.ajax({
			type: 'POST',
			success: function(data) {
				table.row.add(data).draw(false);
				table.page('last').draw(false);
			},
			error: function(){ },
			url: '/container/create/',
			data: data,
			cache: false
		});
	}
});

editor.on( 'preOpen', function ( e, type ) {
	var carrierArray = $.ajax({
		dataType: "json",
		url: '/controlled_list/carrier_type/list.json',
		success: function ( json ) {
		  	editor.field( 'carrier_type' ).update( json.carrierTypes );
		}
	});

	var primaryTypeArray = $.ajax({
		dataType: "json",
		url: '/controlled_list/primary_type/list.json',
		success: function ( json ) {
	  		editor.field( 'primary_type' ).update( json.primaryTypes );
		}
	});

	editor.field('primary_type').val(editor.val('primary_type_identifier'));
	editor.field('carrier_type').val(editor.val('carrier_type_identifier'));
});