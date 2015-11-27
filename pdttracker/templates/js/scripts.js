
$(document).ready(function(){
  $('input[type=text]').addClass('form-control').addClass('input-md');
  $('input[type=password]').addClass('form-control').addClass('input-md');
  $('input[type=number]').addClass('form-control').addClass('input-md');
  $('input[type=submit]').addClass('btn btn-default');
  $('textarea').addClass('form-control').addClass('input-md');
  $('select').addClass('form-control').addClass('input-md');
  $('#id_assign_member').css('list-style-type', 'none');
  $('#id_assign_developer').css('list-style-type', 'none');
  $('#id_assign_member label').addClass('checkbox');
  $('#id_assign_developer label').addClass('checkbox');
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

  	if ( ( $('#pauseTimer').length > 0 || $('#resumeTimer').length > 0 ) && ( $('#pauseTimer').is(':visible') || $('#resumeTimer').is(':visible') ) ) {
  		var url = document.URL;
  		var pattern = url.match(/http:\/\/([a-zA-Z_0-9:\.])+(\/([a-zA-Z0-9_]+))?\/([a-zA-Z0-9_]+)\/([0-9]+)/);
  		var projectId = pattern[5];
	  	$('#pauseTimer').click(function () {
		    $.ajax({
		        url : "/api/pause_timer/" + projectId + "/", // the endpoint
		        type : "GET", // http method
		        //data : { timer : pause }, // data sent with the post request

		        // handle a successful response
		        success : function(json) {
		            console.log(json);
		        },

		        // handle a non-successful response
		        error : function(xhr,errmsg,err) {}
		    });
		});
		$('#resumeTimer').click(function () {
		    $.ajax({
		        url : "/api/resume_timer/" + projectId + "/", // the endpoint
		        type : "GET", // http method
		        //data : { timer : resume }, // data sent with the post request

		        // handle a successful response
		        success : function(json) {
		            console.log(json);
		        },

		        // handle a non-successful response
		        error : function(xhr,errmsg,err) {}
		    });
		});
	}

  if ( $("#switchIteration").length > 0 ) {
    var url = document.URL;
    var pattern = url.match(/http:\/\/([a-zA-Z_0-9:\.])+(\/([a-zA-Z0-9_]+))?\/([a-zA-Z0-9_]+)\/([0-9]+)/);
    var projectId = pattern[5];
    // $('#startPhase').click(function () {
    //     $.ajax({
    //         url : "/api/startPhase/" + projectId + "/", // the endpoint
    //         type : "POST", // http method
    //         data : { "phaseName" : $("#startPhase01").val(), "iterationName": $("#startPhase02").val() }, // data sent with the post request

    //         // handle a successful response
    //         success : function(json) {
    //             console.log(json);
    //         },

    //         // handle a non-successful response
    //         error : function(xhr,errmsg,err) {}
    //     });
    // });
    $('#switchPhase').click(function () {
        $.ajax({
            url : "/api/switchPhase/" + projectId + "/", // the endpoint
            type : "POST", // http method
            data : { "phaseName" : $("#switchPhase01").val(), "iterationName": $("#switchPhase02").val() }, // data sent with the post request

            // handle a successful response
            success : function(json) {
                location.reload();
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {}
        });
    });
    // $('#closeProject').click(function () {
    //     $.ajax({
    //         url : "/api/closeProject/" + projectId + "/", // the endpoint
    //         type : "POST", // http method

    //         // handle a successful response
    //         success : function(json) {
    //             console.log(json);
    //         },

    //         // handle a non-successful response
    //         error : function(xhr,errmsg,err) {}
    //     });
    // });
    // $('#startIteration').click(function () {
    //     $.ajax({
    //         url : "/api/startIteration/" + projectId + "/", // the endpoint
    //         type : "POST", // http method
    //         data : { "iterationName" : $("#startIteration01").val() }, // data sent with the post request

    //         // handle a successful response
    //         success : function(json) {
    //             console.log(json);
    //         },

    //         // handle a non-successful response
    //         error : function(xhr,errmsg,err) {}
    //     });
    // });
console.log('here');
    $('#switchIteration').click(function () {
        console.log('click');
        $.ajax({
            url : "/api/switchIteration/" + projectId + "/", // the endpoint
            type : "POST", // http method
            data : { "sloc" : $("#switchIteration01").val(), "iterationName": $("#switchIteration02").val() }, // data sent with the post request

            // handle a successful response
            success : function(json) {
              console.log('success');
                location.reload();
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
              console.log('error');
            }
        });
    });
    $('#closeProject').click(function () {
        $.ajax({
            url : "/api/startProject/" + projectId + "/", // the endpoint
            type : "POST", // http method
            data : { "sloc" : $("#closeProject01").val() }, // data sent with the post request

            // handle a successful response
            success : function(json) {
                location.reload();
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {}
        });
    });
  }
});