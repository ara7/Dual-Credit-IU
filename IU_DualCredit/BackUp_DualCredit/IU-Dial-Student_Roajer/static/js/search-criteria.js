function student_tab() {
    document.getElementById("student-search-criteria").style.display = "block";
    document.getElementById("enrollment-search-criteria").style.display = "none";
    document.getElementById("course-search-criteria").style.display = "none";
    document.getElementById("footer").setAttribute('style', 'margin-top:40px');

}

function course_tab() {

    // document.getElementById("master-container").setAttribute('style', 'min-height: calc(90vh - 320px);');
    document.getElementById("student-search-criteria").style.display = "none";
    document.getElementById("enrollment-search-criteria").style.display = "none";
    document.getElementById("course-search-criteria").style.display = "block";
    document.getElementById("footer").setAttribute('style', 'margin-top:40px');
}

function enrollment_tab() {
    document.getElementById("enrollment-search-criteria").style.display = "block";
    document.getElementById("student-search-criteria").style.display = "none";
    document.getElementById("course-search-criteria").style.display = "none";
    document.getElementById("footer").setAttribute('style', 'margin-top:40px');

}

function batchexport_tab() {
    document.getElementById("enrollment-search-criteria").style.display = "none";
    document.getElementById("student-search-criteria").style.display = "none";
    document.getElementById("course-search-criteria").style.display = "none";
    document.getElementById("master-container").setAttribute('style', 'min-height:0');
    document.getElementById("footer").setAttribute('style', 'margin-top:213px');
}