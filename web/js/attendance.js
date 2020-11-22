

function start_video() {
  document.getElementById('attendees').innerHTML = '';
  document.getElementById('attendees-count').value = 0;
  var attendanceClass = document.getElementById('live-attendance-class').value;
  if (attendanceClass == "") {
    alert('Please Select Class First')
  }else{
  var cameraType = document.getElementById("camera-type").value;
  if(cameraType == 3) {
    var url = document.getElementById("ip-address").value;
    if (url != '') {
      eel.start_video_py(cameraType, attendanceClass, url);
    }else{
      alert("Please provide the IP address");
      }
  }else{
    eel.start_video_py(cameraType, attendanceClass);
      }
      }

}
function stop_video(){
    eel.stop_video_py();
}

eel.expose(updateImageSrc);
function updateImageSrc(val) {
    let elem = document.getElementById('video');
    elem.src = "data:image/jpeg;base64," + val
}
eel.expose(camera_status);
function camera_status(status_value){
  switch(status_value){
    case 0 : document.getElementById('camera-status').innerText ="Disconnected";
              document.getElementById('camera-status').style.color ="Red";
      break;
    case 1 : document.getElementById('camera-status').innerText ="Connected";
              document.getElementById('camera-status').style.color ="Green";
      break;
    case 2 : document.getElementById('camera-status').innerText ="Camera not found ! Please check and try";
              document.getElementById('camera-status').style.color ="red";
      break;
    case 3 : document.getElementById('camera-status').innerText ="Loading Camera";
              document.getElementById('camera-status').style.color ="Green";
      break;
  }
}

eel.expose(updateAttendance);
function updateAttendance(val) {
    let elem = document.getElementById('attendees');
    elem.innerHTML += "<tr><td>"+val+"</td></tr>";
    var count = parseInt(document.getElementById('attendees-count').value);

    document.getElementById('attendees-count').value = count+1;

}
//show the image name
document.querySelector('#file-upload').addEventListener("change",function(){document.getElementById('file-label').innerText = document.querySelector('#file-upload').files[0].name;});

function uploadPhoto(){
  document.getElementById('attendees').innerHTML = '';
  document.getElementById('attendees-count').value = 0;
  var attendanceClass = document.querySelector("#live-attendance-class").value;
  if (attendanceClass=="" || attendanceClass== null) {
    alert('Please select class first');
  }else{
    //console.log(attendanceClass)
    //alert(attendanceClass);
  var input = document.querySelector("#file-upload");
// change photo to base64
  var file = input.files[0],
    reader = new FileReader();
  reader.onloadend = function () {
    var b64 = reader.result;
    //console.log(b64);
    document.getElementById("video").src = b64;
    eel.photoUpload(b64,attendanceClass);
    //document.getElementById("qr").src = photo_string;
  };
  reader.readAsDataURL(file);
}
}

eel.expose(updatePhotoAttendance);
function updatePhotoAttendance(photo) {
    document.getElementById('video').src = photo;
}

eel.expose(addNewStudentData);
function addNewStudentData(){
  var studentId = document.getElementById("student-id").value;
  add_new_student();

}
document.getElementById('camera-type').addEventListener('change',function(){
  var camtype = document.getElementById('camera-type').value;
  if (camtype==3) {
    document.getElementById('ip-address-group').style.display='block';
  }else{
    document.getElementById('ip-address-group').style.display='none';
  }
});