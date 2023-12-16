window.addEventListener("DOMContentLoaded", async () => {
  const workdragList = document.getElementById("work-list");

  reorderWorkList();

  window.work_drag = {};
  window.work_drag.draggedItem = null;

  // Add event listeners for drag and drop events
  workdragList.addEventListener("dragstart", workHandleDragStart);
  workdragList.addEventListener("dragover", workHandleDragOver);
  workdragList.addEventListener("drop", workHandleDrop);
});

// Drag start event handler
function workHandleDragStart(event) {
  window.work_drag.draggedItem = event.target;
  event.dataTransfer.effectAllowed = "move";
  event.dataTransfer.setData("text/html", window.work_drag.draggedItem.innerHTML);
  event.target.style.opacity = "0.5";
}

// Drag over event handler
function workHandleDragOver(event) {
  event.preventDefault();
  event.dataTransfer.dropEffect = "move";
  const targetItem = event.target;
  if (targetItem !== window.work_drag.draggedItem && targetItem.classList.contains("drag-item")) {
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
function workHandleDrop(event) {
  event.preventDefault();
  const targetItem = event.target;
  if (targetItem !== window.work_drag.draggedItem && targetItem.classList.contains("drag-item")) {
    if (event.clientY > targetItem.getBoundingClientRect().top + targetItem.offsetHeight / 2) {
      targetItem.parentNode.insertBefore(window.work_drag.draggedItem, targetItem.nextSibling);
    } else {
      targetItem.parentNode.insertBefore(window.work_drag.draggedItem, targetItem);
    }
  }
  targetItem.style.borderTop = "";
  targetItem.style.borderBottom = "";
  window.work_drag.draggedItem.style.opacity = "";
  window.work_drag.draggedItem = null;

  const user_id = document.getElementById("user-id-info").value;
  const workdragList = document.getElementById("work-list");

  const workIds = []
  
  for (const dragli of workdragList.children) {
    workIds.push(dragli.id.split('-')[2])
  }

  const values = {}
  values.userId = user_id
  values.workIds = workIds

  fetch('/api/v1/work/ordering/', {
    method: "PUT",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(values)
  })
}

async function reorderWorkList() {
  const user_id = document.getElementById("user-id-info").value;

  const workdragList = document.getElementById("work-list");

  const ordering = await fetch(`/api/v1/ordering/${user_id}/`)
    .then(validateJSON)
    .catch((error) => {
      console.log("Error Fetching Work Order Data: ", error);
    });

  const newDragList = []
  for (const id of ordering.work){
    newDragList.push(document.getElementById(`work-li-${id}`))
  }

  workdragList.replaceChildren(...newDragList)
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
