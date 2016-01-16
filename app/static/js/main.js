$(document).ready(function () {
    // Pretty-print all JSON debugging info
    $('pre').each(function () {
        $(this).text(JSON.stringify(JSON.parse($(this).text()), null, 2));
    });

    // Attach event to handle checkmark click events
    $('body').on('click', '.add, .remove', function () {
        var action = $(this).attr('class').indexOf('add') > -1 ? 'add' : 'remove';
        var parent = $(this).parent();
        var id = parent.attr('obj-id');
        var type = parent.attr('obj-type');
        var counter = parent.find('.counter');
        var url = INTEREST_POST_URL.replace('/type', '/' + type).replace('/id', '/' + id);
        var post_data = { action: action, attribute: null };
        var that = $(this);

        $.ajax({
            type: 'POST',
            url: url,
            data: post_data,
            dataType: 'json'
        })
        .success(function (data) {
            if (action === 'add') {
                that.removeClass('add');
                that.addClass('remove');
            }
            else {
                that.addClass('add');
                that.removeClass('remove');
            }
        }).error(function (data) {
            console.log(data);
        });
    });
});