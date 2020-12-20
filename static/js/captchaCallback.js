function enableScrapsFormSubmission(token) {
  const currentSubmitBtn = document.querySelector("#scraps-form-btn");
  if (currentSubmitBtn) {
    return false;
  }
  const form = document.querySelector(".scraps-form");
  const submitBtn = document.createElement("button");
  submitBtn.classList.add("btn");
  submitBtn.classList.add("btn-info");
  submitBtn.classList.add("btn-lg");
  submitBtn.innerText = "Submit";
  if (window.location.pathname == "/crawl") {
    submitBtn.type = "button";
  } else {
    submitBtn.type = "submit";
  }
  submitBtn.id = "scraps-form-btn";
  form.appendChild(submitBtn);
  if (token) {
    console.log(token);
  }
}
