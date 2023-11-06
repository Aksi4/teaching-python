document.addEventListener("DOMContentLoaded", function() {
    var closeButton = document.getElementById("close-button");
    var alert = document.querySelector(".alert");

    closeButton.addEventListener("click", function() {
        alert.style.display = "none";
    });
});