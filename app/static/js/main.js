$(document).ready(function () {
    // Pretty-print all JSON debugging info
    $('pre').each(function () {
        $(this).text(JSON.stringify(JSON.parse($(this).text()), null, 2));
    });

    // Attach event to handle checkmark click events
    $('body').on('click', '.add.button.glyphicon.glyphicon-ok, .remove.button.glyphicon.glyphicon-ok', function () {
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

    // At the start of the page, update the interested status of all checkmarks
    $('.button.glyphicon.glyphicon-ok').each(function () {
        var parent = $(this).parent();
        var id = parent.attr('obj-id');
        var type = parent.attr('obj-type');
        var userID = $('#body').attr('data-user-id');

        var url = "/users/" + userID + "/" + type + "s/" + id + "/" + type + "_get_interested_status";
        var that = $(this);

        $.ajax({
            type: 'GET',
            url: url,
            dataType: 'json'
        }).success(function (data) {
            if (data === true) {
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

    // At the start of the page, update the interested status of all toggle buttons
    var interestedToggle = $('#interested-toggle');
    var interested = interestedToggle.find('label:first');
    var notInterested = interestedToggle.find('label:nth-child(2)');
    var id = interestedToggle.attr('obj-id');
    var type = interestedToggle.attr('obj-type');
    var userID = $('#body').attr('data-user-id');
    var url = "/users/" + userID + "/" + type + "s/" + id + "/" + type + "_get_interested_status";
    if (url.indexOf('undefined') === -1 && url.indexOf('//') === -1) {
        $.ajax({
            type: 'GET',
            url: url,
            dataType: 'json'
        }).success(function (data) {
            if (data === true) {
                interested.addClass('active');
                notInterested.removeClass('active');
            }
            else {
                notInterested.addClass('active');
                interested.removeClass('active');
            }
        }).error(function (data) {
            console.log(data);
        });
    }
    else {
        // If we can't figure it out, let's just set the user to not interested
        notInterested.addClass('active');
        interested.removeClass('active');
    }

});