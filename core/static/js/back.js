/**
 * This is for back button reserves since kinda refresh all the page of django and i dont want that
 */

const button = document.getElementById("backButton");
const buttonOne = document.getElementById("backButton1");

if (button) {
  button.addEventListener("click", function (e) {
    e.preventDefault();
    history.back();
  });
}

if (buttonOne) {
  buttonOne.addEventListener("click", function (e) {
    e.preventDefault();
    history.back();
  });
}
