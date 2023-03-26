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

function setCookie(name, value, days) {
  let expires = "";
  if (days) {
    let date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
  const cookieName = `; ${document.cookie}`;
  const parts = cookieName.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}