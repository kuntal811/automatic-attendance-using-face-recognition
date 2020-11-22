document.querySelector('#login-form').addEventListener('submit',function(event){
	event.preventDefault();
	var userName = document.getElementById('login').value;
	var password = document.getElementById('password').value;
	if (userName!="" && password!="") {
	eel.teacher_login(userName,password);
}
});
eel.expose(login_success);
function login_success(url){
	location.replace(url);
}
eel.expose(login_error);
function login_error(error_msg){
	document.getElementById('error-msg').innerText = error_msg;
}
