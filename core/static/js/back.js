const button = document.getElementById("backButton");

button.addEventListener("click", function (e) {
  e.preventDefault();
  history.back();
});
