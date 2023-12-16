window.addEventListener("DOMContentLoaded", async () => {
  reorderLangList();
  reorderWorkList();
});

async function reorderLangList() {
  const user_id = document.getElementById("user-id-info").value;

  const langdragList = document.getElementById("language-list");

  const ordering = await fetch(`/api/v1/ordering/${user_id}/`)
    .then(validateJSON)
    .catch((error) => {
      console.log("Error Fetching Language Order Data: ", error);
    });

  console.log(ordering);

  const newDragList = [];
  for (const id of ordering.lang) {
    newDragList.push(document.getElementById(`lang-li-${id}`));
  }

  langdragList.replaceChildren(...newDragList);
}

async function reorderWorkList() {
  const user_id = document.getElementById("user-id-info").value;

  const workdragList = document.getElementById("work-list");

  const ordering = await fetch(`/api/v1/ordering/${user_id}/`)
    .then(validateJSON)
    .catch((error) => {
      console.log("Error Fetching Work Order Data: ", error);
    });

  const newDragList = [];
  for (const id of ordering.work) {
    newDragList.push(document.getElementById(`work-li-${id}`));
  }

  workdragList.replaceChildren(...newDragList);
}

/**
 * Validate a response to ensure the HTTP status code indcates success.
 *
 * @param {Response} response HTTP response to be checked
 * @returns {object} object encoded by JSON in the response
 */
function validateJSON(response) {
  if (response.ok) {
    return response.json();
  } else {
    return Promise.reject(response);
  }
}
