document.getElementById('sidebar-hide').addEventListener("click",hideSidebar);
function hideSidebar(){
  document.getElementById('sidebar').style.display='none';
}
document.getElementById('sidebar-show').addEventListener("click",showSidebar);
function showSidebar(){
  document.getElementById('sidebar').style.display='block';
}


eel.get_user_details()(showUserDetails);
function showUserDetails(userName){
document.getElementById('admin-name').innerText=userName;
}
eel.expose(logout);
function logout(){
  alert("Logout Successfully");
  window.location.href = 'login.html';
}

function show_image() {
	eel.show_image()(setImage);
}

function setImage(base64) {
	document.getElementById("qr").src = base64;
}


/*eel.expose(updatePhotoAttendance);
function updatePhotoAttendance(photo) {
    document.getElementById('qr').src = photo;
}*/


/*var input = document.querySelector('input[type=file]');

// You will receive the Base64 value every time a user selects a file from his device
// As an example I selected a one-pixel red dot GIF file from my computer
input.onchange = function () {
  var file = input.files[0],
    reader = new FileReader();

  reader.onloadend = function () {
    // Since it contains the Data URI, we should remove the prefix and keep only Base64 string
    var b64 = reader.result.replace(/^data:.+;base64,/, '');
    console.log(b64); //-> "R0lGODdhAQABAPAAAP8AAAAAACwAAAAAAQABAAACAkQBADs="
  };

  reader.readAsDataURL(file);
};*/