$(document).ready(function () {
    // Pretty-print all JSON debugging info
    $('pre').each(function () {
        $(this).text(JSON.stringify(JSON.parse($(this).text()), null, 2));
    });    
});