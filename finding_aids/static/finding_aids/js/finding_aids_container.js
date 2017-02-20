var editor = new $.fn.dataTable.Editor( {
	ajax: "/finding_aids/editor_update/",
	table: "#fa_table",
	fields: [
		{
			label: "Folder/Item Number",
			name: "entity_no",
			type: "readonly"
		}, {
			label: "Level",
			name:  "level",
			type:  "radio",
		    options: [
        		'Folder',
        		'Item'
    		]
		}, {
			label: "Title",
			name: "title"
		}, {
			label: "Original Title",
			name: "title_original"
		}, {
			label: "Original Language",
			name: "original_locale",
			type: "select"
		}, {
			label: "Date From",
			name: "date_from"
		}, {
			label: "Date To",
			name: "date_to"
		}
	]
});

// DataTable Init
var table = $('#fa_table').DataTable({
    "dom": "Blrtip",
	"serverSide": true,
	"ajax": "/finding_aids/datatable/" + containerID ,
	"select": true,
	"columns": [
	   { "data": 'entity_no', "width": "10%", "class": "action_column reorder" },
	   { "data": 'title', "width": "30%" },
	   { "data": 'title_original', "width": "30%" },
	   { "data": 'date_from', "width": "10%" },
	   { "data": 'date_to', "width": "10%" },
	],
	"buttons": [
		{
			"extend": "create",
			"editor": editor,
			formButtons: [
				{ label: 'Close', fn: function () { this.close(); }, className: "pull-left" },
				{ label: 'Save', fn: function () { this.submit(); }, className: 'btn-editor btn-primary'}
			],
			"text": '<i class="fa fa-plus"></i> Quick Create',
			"className": 'btn-default'
		}, {
			"extend": "edit",
			"editor": editor,
			formButtons: [
				{ label: 'Close', fn: function () { this.close(); }, className: "pull-left" },
				{ label: 'Save', fn: function () { this.submit(); }, className: 'btn-editor btn-primary'}
			],
			"text": '<i class="fa fa-edit"></i> Quick Edit',
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
		"dataSrc": 'entity_no',
        "editor":  editor,
		"update": false
    },
	"lengthMenu": [ [10, 25, 50, -1], [10, 25, 50, "All"] ],
	"paging":   true,
    "ordering": false,
    "info":     false,
	"searching": false,
	"autoWidth": true
});