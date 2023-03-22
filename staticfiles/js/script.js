function navigateForm() {
    var input = document.getElementsByName("job_title")[0].value;
    if (input == "") {
      alert("Please enter a job title");
      return false;
    }
    var url = "/salary/" + encodeURIComponent(input) + "/";
    window.location.href = url;
    return false;
}