function enableScrapsFormSubmission(token) {
  if (!token) {
    return false;
  }
  const currentSubmitBtn = document.querySelector("#scraps-form-btn");
  if (currentSubmitBtn) {
    return false;
  }
  const btn = createFormSubmit();
  const form = document.querySelector(".scraps-form");
  form.appendChild(btn);
}

function createFormSubmit() {
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
  return submitBtn;
}
