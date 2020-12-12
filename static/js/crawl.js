window.addEventListener("load", () => {
  const form = document.querySelector("#crawl-form");
  const formBtn = document.querySelector("#crawl-form-button");
  const crawlResponse = document.querySelector("#crawl-response");
  const crawlResponseText = document.querySelector("#crawl-response__text");

  function processCrawlReqeust() {
    if (form.checkValidity()) {
      const formData = new FormData(form);
      postFormData(`${window.location.origin}/crawl`, formData)
        .then((data) => {
          console.log(data);
          showCrawlResponse(data.message, "crawl-response__success");
          form.reset();
        })
        .catch((error) => {
          showCrawlResponse(error.message, "crawl-response__error");
        });
    } else {
      showCrawlResponse("Invalid form submission", "crawl-response__error");
    }
  }

  async function postFormData(url, data) {
    const token = data.get("csrf_token");
    let response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": token,
      },
      body: data,
    });
    return response.json();
  }

  function showCrawlResponse(errorText, responseClass) {
    crawlResponse.classList.add(responseClass);
    crawlResponseText.innerHTML = errorText;
    crawlResponse.classList.add("crawl-response__active");
    window.setTimeout(function () {
      crawlResponse.classList.remove("crawl-response__active");
      crawlResponse.classList.remove(responseClass);
      crawlResponseText.textContent = "";
    }, 4000);
  }

  formBtn.addEventListener("click", processCrawlReqeust);
});
