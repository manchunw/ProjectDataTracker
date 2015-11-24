
$(document).ready(function(){
  $('input[type=text]').addClass('form-control').addClass('input-md');
  $('input[type=password]').addClass('form-control').addClass('input-md');

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