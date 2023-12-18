window.addEventListener("DOMContentLoaded", async () => {
  const projectDivs = document.getElementsByClassName("project-container");

  // Options for the observer (which mutations to observe)
  const config = { attributes: true, childList: true, subtree: true };

  // Callback function to execute when mutations are observed
  const callback = (mutationList, observer) => {
    for (const mutation of mutationList) {
      if (mutation.type === "childList") {
        console.log("A child node has been added or removed.");
      } else if (mutation.type === "attributes") {
        saveProjects();
      }
    }
  };

  // Create an observer instance linked to the callback function
  const observer = new MutationObserver(callback);

  for (const projectDiv of projectDivs) {
    const id = projectDiv.id.split("-")[2];
    const title = document.getElementById(`project-title-${id}`);
    const description = document.getElementById(`project-description-${id}`);
    const link = document.getElementById(`project-link-${id}`);

    observer.observe(title, config);
    observer.observe(description, config);
    observer.observe(link, config);
  }
});

async function saveProjects() {
  const projectDivs = document.getElementsByClassName("project-container");
  const user_id = document.getElementById("user-id-info").value;

  for (const projectDiv of projectDivs) {
    const id = projectDiv.id.split("-")[2];
    const title = document.getElementById(`project-title-${id}`).innerText;
    const description = document.getElementById(`project-description-${id}`).innerText;
    const link = document.getElementById(`project-link-${id}`).innerText;

    saveProject(id, title, description, link, user_id);
  }
}

async function saveProject(id, title, description, link, user_id) {
  const data = new FormData();
  data.append("title", title);
  data.append("description", description);
  data.append("link", link);
  data.append("userId", user_id);

  fetch(`/api/project/${id}/`, {
    method: "PUT",
    body: data,
  });
}
