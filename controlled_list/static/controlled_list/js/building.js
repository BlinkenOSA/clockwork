var editor = new $.fn.dataTable.Editor( {
	ajax: "update-ajax",
	table: "#building_table",
	fields: [ {
			label: "Building Name",
			name: "building"
		}],
    formOptions: {
        inline: {
           onBlur: 'submit'
        }
    }
} );

$('#building_table').dataTable({
	"serverSide": true,
	"ajax": "datatable",
    "keys": {
        columns: ':not(:first-child)',
        editor:  editor
    },
    select: {
        style:    'os',
        selector: 'td:first-child',
        blurable: true
    },
});

$('#building_table').on( 'click', 'tbody td:not(:first-child)', function (e) {
	editor.bubble( this );
} );
