var myForm = document.forms.namedItem("myForm");

myForm.addEventListener("submit", function (e) {
    e.preventDefault();

    let id = document.getElementById("Student_id").value;
    let name = document.getElementById("Student_name").value;
    let email = document.getElementById("Email").value;
    let department = document.getElementById("Department").value;
    let file = document.getElementById("jpg").value;

    var formdata = new FormData(document.getElementById("myForm"));
    fetch("http://IP:5055/Store", {
        method: "POST",
        body: formdata,
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            render(data);
        })
        .catch((error) => console.log("error", error));
});

function render(data) {
    window.location.replace("./profile/profile.html");
}
