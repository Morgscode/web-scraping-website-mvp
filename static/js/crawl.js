window.addEventListener("load", () => {
  const form = document.querySelector("#crawl-form");
  const downloadLink = document.querySelector("#download-link");
  const downloadLinkWrapper = document.querySelector("#download-wrapper");
  const crawlResponse = document.querySelector("#crawl-response");
  const crawlResponseText = document.querySelector("#crawl-response__text");

  function processCrawlReqeust(e) {
    if (e.target && e.target.id !== "scraps-form-btn") {
      return false;
    }
    hideDownloadInterface();
    if (form.checkValidity()) {
      showCrawlResponse(
        "okay, crawling the web now...",
        "crawl-response__crawling"
      );
      const json = convertFormDataToJson(form);
      postFormData(`${window.location.origin}/crawl`, json, form)
        .then((data) => {
          let responseClass = assignResponseClassByStatusCode(data.statusCode);
          showCrawlResponse(data.message, responseClass);
          showDownloadInterface(data.downloadUrl);
          form.reset();
          // console.log(data);
        })
        .catch((error) => {
          // console.log(error);
          showCrawlResponse(
            "there was a problem crawling the site",
            "crawl-response__error",
            4000
          );
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
    postData = new Object();
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

  function assignResponseClassByStatusCode(statusCode) {
    return statusCode === 200
      ? "crawl-response__success"
      : "crawl-response__error";
  }

  function showCrawlResponse(responseText, responseClass, responseTimeout) {
    hideCrawlResponse();
    crawlResponseText.innerHTML = responseText;
    crawlResponse.classList.add(responseClass, "crawl-response__active");
    if (responseTimeout) {
      window.setTimeout(function () {
        hideCrawlResponse();
      }, responseTimeout);
    }
  }

  function hideCrawlResponse() {
    crawlResponse.className = "";
    crawlResponseText.textContent = "";
  }

  function showDownloadInterface(url) {
    downloadLink.href = url;
    downloadLinkWrapper.classList.add("download-active");
    downloadLinkWrapper.scrollIntoView();
  }

  function hideDownloadInterface() {
    downloadLink.href = "";
    downloadLinkWrapper.classList.remove("download-active");
  }

  form.addEventListener("click", processCrawlReqeust);
});
