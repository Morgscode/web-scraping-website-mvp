window.addEventListener("load", () => {
  const form = document.querySelector("#crawl-form");
  const formBtn = document.querySelector("#crawl-form-button");
  const crawlResponse = document.querySelector("#crawl-response");
  const crawlResponseText = document.querySelector("#crawl-response__text");

  function processCrawlReqeust() {
    if (form.checkValidity()) {
      const json = convertFormDataToJson(form);
      postFormData(`${window.location.origin}/crawl`, json, form)
        .then((data) => {
          let responseClass = assignResponseClassByStatusCode(data.statusCode);
          showCrawlResponse(data.message, responseClass);
          form.reset();
          console.log(data);
        })
        .catch((error) => {
          console.log(error);
          showCrawlResponse(error.message, "crawl-response__error", 4000);
        });
    } else {
      showCrawlResponse(
        "Invalid form submission",
        "crawl-response__error",
        4000
      );
    }
  }

  function convertFormDataToJson(form) {
    const formData = new FormData(form);
    postData = {};
    formData.forEach((value, key) => (postData[key] = value));
    const json = JSON.stringify(postData);
    return json;
  }

  async function postFormData(url, data, form) {
    const token = new FormData(form).get("csrf_token");
    let response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": token,
      },
      body: data,
    });
    return response.json();
  }

  function showCrawlResponse(responseText, responseClass, responseTimeout) {
    hideCrawlResponse();
    crawlResponse.classList.add(responseClass);
    crawlResponseText.innerHTML = responseText;
    crawlResponse.classList.add("crawl-response__active");
    if (responseTimeout) {
      window.setTimeout(function () {
        hideCrawlResponse();
      }, responseTimeout);
    }
  }

  function hideCrawlResponse() {
    crawlResponse.classList.remove("crawl-response__active");
    crawlResponse.className = "";
    crawlResponseText.textContent = "";
  }

  function assignResponseClassByStatusCode(statusCode) {
    return statusCode === 200
      ? "crawl-response__success"
      : "crawl-response__error";
  }

  formBtn.addEventListener("click", processCrawlReqeust);
});
