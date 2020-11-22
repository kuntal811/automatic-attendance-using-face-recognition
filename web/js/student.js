function addNewStudent(){
	document.getElementById("add-new-student").style.display="block";
	document.getElementById("display").style.display="none";
	document.getElementById("add-new-student-photo").style.display="block";
}
function studentData(){
	document.getElementById("add-new-student").style.display="none";
	document.getElementById("display").style.display="block";
	document.getElementById("add-new-student-photo").style.display="none";
}

function startVideoForCapture(){
	/*var elm = document.getElementById("photo-capture-start");
	elm.classList.remove('d-block');
	elm.classList.add('d-none');*/
	var studentId =document.getElementById('student-id').value
	var ipAddress = document.getElementById('ip-address').value;
	if (studentId == '') {
		alert('First fill the form then capture photo')
	}else if (ipAddress == "") {
		alert('Default camera is beeing used');
		eel.capture_photo_py(0);
		document.getElementById("photo-capture-stop").classList.add('d-block');
		document.getElementById("photo-capture").classList.add('d-block');
		var elm = document.getElementById("submit-student-data");
		elm.classList.remove('d-none');
		elm.classList.add('d-block');		
	}else{
		eel.capture_photo_py(ipAddress);
		document.getElementById("photo-capture-stop").classList.add('d-block');
		document.getElementById("photo-capture").classList.add('d-block');
		var elm = document.getElementById("submit-student-data");
		elm.classList.remove('d-none');
		elm.classList.add('d-block');
	}
}
function stop_video(){
	var elm = document.getElementById("photo-capture-stop");
	elm.classList.remove('d-block');
	elm.classList.add('d-none');
	var elm = document.getElementById("photo-capture");
	elm.classList.remove('d-block');
	elm.classList.add('d-none');
	eel.stop_video_py();
	document.getElementById("photo-capture-start").classList.remove('d-none');
	document.getElementById("photo-capture-start").classList.add('d-block');
}

eel.expose(updateStudentImageSrc);
function updateStudentImageSrc(photo){
	document.getElementById('video').src = "data:image/jpeg;base64," + photo;
}
function capturePhoto(){
	var studentId =document.getElementById('student-id').value
	if (studentId == '') {
		alert('First fill the form then capture photo')
	}else{
		eel.save_photo(studentId);
	}
}
eel.expose(showCapturePhoto);
function showCapturePhoto(capturedPhoto){
	document.getElementById('captured-photo').innerHTML += "<img src = 'data:image/jpeg;base64," + capturedPhoto+"'style='height:50px;width:50px;' class='col-sm-4 mb-2'>";
}

function submitStudentData(){
	var stu_id 		  = document.getElementById("student-id").value;
	var fullname 	  = document.getElementById("name").value;
	var student_class = document.getElementById("student-class").value;
	var session		  = document.getElementById("session").value;
	if (stu_id == "" || fullname == "" ||student_class == "" || session == ""){
		alert("Fill the form first");
	}else{
	document.getElementById('message').innerHTML = "<p class='text-success'>Saving data...</p>"
	eel.submit_student_data(stu_id, fullname, student_class, session);
}
}

eel.expose(failed_data_submit);
function failed_data_submit(){
	document.getElementById('message').innerText ="Failed to save data";
	document.getElementById('message').style.color="red";
}
eel.expose(student_data_saved);
function student_data_saved(){
	document.getElementById('message').innerText ="Data Saved Successfully";
	document.getElementById('message').style.color="Green";
}

function showStudentDataTable(){
	var searchClassData = document.getElementById('search-class-data').value;
	if (searchClassData == "") {
		alert('Please Select Class First');
	}else{
		document.getElementById('student-data-table').innerHTML = "";
		eel.fetch_class_data(searchClassData);
	}
}
eel.expose(setTableData);
function setTableData(studentId,name,student_class,session){
	onclicktask = "deleteStudent('"+studentId+"');";
	document.getElementById('student-data-table').innerHTML +="<tr id='"+studentId+"'><th scope='row'>"+studentId+"</th><td>"+name+"</td><td>"+student_class+"</td><td>"+session+"</td><td><a href='#' onclick="+onclicktask+"><i class='fas fa-trash text-danger'> Delete</i></a></td></tr>";
}
function deleteStudent(studentId){
	eel.deleteStudent(studentId);
}
eel.expose(deleteStatus);
function deleteStatus(student_id){
	if (student_id != "") {
		document.getElementById(student_id).remove();
	}else{
		alert("failed to delete student data");
	}
}

