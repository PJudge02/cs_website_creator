window.addEventListener("DOMContentLoaded", async () => {
  const langdragList = document.getElementById("language-list");

  reorderLangList();

  window.lang_drag = {};
  window.lang_drag.draggedItem = null;

  // Add event listeners for drag and drop events
  langdragList.addEventListener("dragstart", langHandleDragStart);
  langdragList.addEventListener("dragover", langHandleDragOver);
  langdragList.addEventListener("drop", langHandleDrop);
});

// Drag start event handler
function langHandleDragStart(event) {
  window.lang_drag.draggedItem = event.target;
  event.dataTransfer.effectAllowed = "move";
  event.dataTransfer.setData("text/html", window.lang_drag.draggedItem.innerHTML);
  event.target.style.opacity = "0.5";
}

// Drag over event handler
function langHandleDragOver(event) {
  event.preventDefault();
  event.dataTransfer.dropEffect = "move";
  const targetItem = event.target;
  if (targetItem !== window.lang_drag.draggedItem && targetItem.classList.contains("drag-item")) {
    const boundingRect = targetItem.getBoundingClientRect();
    const offset = boundingRect.y + boundingRect.height / 2;
    if (event.clientY - offset > 0) {
      targetItem.style.borderBottom = "solid 2px #000";
      targetItem.style.borderTop = "";
    } else {
      targetItem.style.borderTop = "solid 2px #000";
      targetItem.style.borderBottom = "";
    }
  }
}

// Drop event handler
function langHandleDrop(event) {
    console.log("Here")
  event.preventDefault();
  const targetItem = event.target;
  if (targetItem !== window.lang_drag.draggedItem && targetItem.classList.contains("drag-item")) {
    if (event.clientY > targetItem.getBoundingClientRect().top + targetItem.offsetHeight / 2) {
      targetItem.parentNode.insertBefore(window.lang_drag.draggedItem, targetItem.nextSibling);
    } else {
      targetItem.parentNode.insertBefore(window.lang_drag.draggedItem, targetItem);
    }
  }
  targetItem.style.borderTop = "";
  targetItem.style.borderBottom = "";
  window.lang_drag.draggedItem.style.opacity = "";
  window.lang_drag.draggedItem = null;

  const user_id = document.getElementById("user-id-info").value;
  const langdragList = document.getElementById("language-list");

  const langIds = [];

  for (const dragli of langdragList.children) {
    langIds.push(dragli.id.split("-")[2]);
  }

  const values = {};
  values.userId = user_id;
  values.languageIds = langIds;

  fetch("/api/v1/language/ordering/", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(values),
  });
}

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
