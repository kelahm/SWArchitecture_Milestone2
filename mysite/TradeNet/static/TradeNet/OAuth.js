//after successful google signin this function is called
function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
	console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
	console.log('Name: ' + profile.getName());
	console.log('Image URL: ' + profile.getImageUrl());
	console.log('Email: ' + profile.getEmail());
	
	var csrftoken = getCookie('csrftoken');
	id_token = googleUser.getAuthResponse().id_token;
	var xhr = new XMLHttpRequest();
	xhr.open('POST', 'http://localhost:8000/TradeNet/tokensignin');
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	xhr.setRequestHeader("X-CSRFToken", csrftoken);
	xhr.onload = function() {
		console.log('Signed in: ' + xhr.responseText);
		location.reload();
	};
	xhr.send('idtoken=' + id_token);
}

//signs the user out of thier google account
function signOut() {
	var auth2 = gapi.auth2.getAuthInstance();
	auth2.signOut().then(function () {
		window.location.replace("http://localhost:8000/TradeNet/logout");
	});
}

function onLoad() {
  gapi.load('auth2', function() {
	gapi.auth2.init();
  });
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}