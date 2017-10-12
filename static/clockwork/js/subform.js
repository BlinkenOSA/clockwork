var subformCreate = function(prefix) {
    var classname = '.' + prefix + '-subform';
    var addCssClass = prefix + '-add-row';
    var deleteCssClass = prefix + '-delete-row';
    var formCssClass = prefix + '-form';

    $(classname).formset({
        prefix: prefix,
        addText: 'Add',
	    deleteText: 'Remove',
        addCssClass: addCssClass,
        deleteCssClass: deleteCssClass,
        formCssClass: formCssClass
    })

    $('.delete-row-hidden').hide();
};