// This can be called on dynamically created elements too
function bind_interested($container) {
	function send_interest(id, action, mode, $counter) {
		post_data = { action: action, attribute: mode };
		console.log(post_data);
		$.post( INTEREST_POST_URL.replace('id',id), post_data, function( data ) {
			console.log(data);
			// Counter within the interested widget
		  $counter.text(data.num_interested);
		  // Controlling counters detached from the buttons
		  $('.counter.'+id).text(data.num_interested);
		}, "json").fail(function() {
			// Assume failure is a 302 from being an anonymous user
    	window.location.href=INTEREST_LOGIN_URL.replace('id',id);
  	});
	}
	// add
	$container.on('click', '.interested .add.button', function() {
		$p = $(this).parent();
		id = $p.attr('proposal-id');
		send_interest( id, 'add', null, $p.find('.counter'));
		$p.find('.remove').addClass('button');
    $p.find('.add').removeClass('button');
	});
	// remove
	$container.on('click', '.interested .remove.button', function() {
		$p = $(this).parent();
		id = $p.attr('proposal-id');
		send_interest( id, 'remove', null, $p.find('.counter'));
		$p.find('.add').addClass('button');
    $p.find('.remove').removeClass('button');
	});
}


$(document).ready(function() {
	bind_interested($(document));
})