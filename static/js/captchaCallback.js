function enableScrapsFormSubmission(token) {
  const form = document.querySelector(".scraps-form");
  const submitBtn = document.createElement("button");
  submitBtn.classList.add("btn");
  submitBtn.classList.add("btn-info");
  submitBtn.classList.add("btn-lg");
  submitBtn.innerText = "Submit";
  submitBtn.type = "button";
  submitBtn.id = "scraps-form-btn";
  form.appendChild(submitBtn);
  if (token) {
    console.log(token);
  }
}
