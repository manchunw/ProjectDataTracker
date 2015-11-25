
$(document).ready(function(){
  $('input[type=text]').addClass('form-control').addClass('input-md');
  $('input[type=password]').addClass('form-control').addClass('input-md');
  $('input[type=number]').addClass('form-control').addClass('input-md');
  $('input[type=submit]').addClass('btn btn-default');
  $('textarea').addClass('form-control').addClass('input-md');
  $('select').addClass('form-control').addClass('input-md');
  $('#id_assign_member').css('list-style-type', 'none');
  $('#id_assign_member label').addClass('checkbox');
  if ($('ul.pagination').length) {
  	if ($('ul.pagination > li.previous').length == 0) {
  		$('ul.pagination').prepend('<li class="previous col-xs-4">&nbsp;<li>');
  	} else {
  		$('ul.pagination > li.previous').addClass('col-xs-4');
  		$('ul.pagination > li.previous > a').addClass('pull-right');
  	}
  	if ($('ul.pagination > li.next').length == 0) {
  		$('ul.pagination').append('<li class="next col-xs-4 text-left">&nbsp;<li>');
  	} else {
  		$('ul.pagination > li.next').addClass('col-xs-4');
  	}
  	$('ul.pagination > li.current').addClass('col-xs-4 text-center');
  	$('ul.pagination > li.cardinality').addClass('col-xs-12');
  	$('ul.pagination').addClass('col-xs-12');
  }

  $('#pauseTimer').click(function () {
	    console.log("pause_time is called!") // sanity check
	    $.ajax({
	        url : "/api/command/", // the endpoint
	        type : "POST", // http method
	        //data : { timer : pause }, // data sent with the post request

	        // handle a successful response
	        success : function(json) {
	            //$('#post-text').val(''); // remove the value from the input
	            console.log(json); // log the returned json to the console
	            //console.log("success"); // another sanity check
	        },

	        // handle a non-successful response
	        error : function(xhr,errmsg,err) {}
	    });
	});
	$('#resumeTimer').click(function () {
	    console.log("resume_time is called!") // sanity check
	    $.ajax({
	        url : "/api/command/", // the endpoint
	        type : "POST", // http method
	        //data : { timer : resume }, // data sent with the post request

	        // handle a successful response
	        success : function(json) {
	            //$('#post-text').val(''); // remove the value from the input
	            console.log(json); // log the returned json to the console
	            //console.log("success"); // another sanity check
	        },

	        // handle a non-successful response
	        error : function(xhr,errmsg,err) {}
	    });
	});
});