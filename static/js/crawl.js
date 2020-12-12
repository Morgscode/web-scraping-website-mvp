window.addEventListener("load", function () {
  var form = document.querySelector("#crawl-form");
  var formBtn = document.querySelector("#crawl-form-button");
  var crawlResponse = document.querySelector("#crawl-response");
  var crawlResponseText = document.querySelector("#crawl-response__text");

  function processCrawlReqeust() {
    if (form.checkValidity()) {
      var formData = new FormData(form);
      formData.forEach(function (field) {
        console.log(field);
      });
    } else {
      showCrawlError("Invalid form submission");
    }
  }

  async function postFormData(url, data) {
    const response = await fetch(url, {
      method: "POST",
    });
  }

  function showCrawlError(error) {
    crawlResponse.classList.add("crawl-response__error");
    crawlResponseText.innerHTML = error;
    crawlResponse.classList.add("crawl-response__active");
    window.setTimeout(function () {
      crawlResponse.classList.remove("crawl-response__active");
      crawlResponse.classList.remove("crawl-response__error");
      crawlResponseText.textContent = "";
    }, 4000);
  }

  formBtn.addEventListener("click", processCrawlReqeust);
});
