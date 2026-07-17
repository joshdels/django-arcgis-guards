const addButton = document.getElementById("add-deployment");
const container = document.getElementById("deployment-forms");
const template = document.getElementById("empty-form");

addButton.addEventListener("click", () => {
  const totalForms = document.getElementById("id_form-TOTAL_FORMS");

  const formIndex = Number(totalForms.value);

  let html = template.innerHTML;

  html = html.replace(/__prefix__/g, formIndex);

  container.insertAdjacentHTML("beforeend", html);

  totalForms.value = formIndex + 1;

  updateTitles();
});

function updateTitles() {
  const cards = document.querySelectorAll(".deployment-card");

  cards.forEach((card, index) => {
    card.querySelector("h3").textContent = `Deployment ${index + 1}`;
  });
}

updateTitles();
