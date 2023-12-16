window.addEventListener("DOMContentLoaded", async () => {
  const new_proj_btn = document.getElementById("save-new-project-btn");
  new_proj_btn.addEventListener("click", new_proj);

  window.project_create = {}
  window.project_create.file = null;
});

async function new_proj() {
  const user_id = parseInt(document.getElementById("user-id-info").value);
  const proj_title = document.getElementById("new-project-title-input").value;
  const proj_discription = document.getElementById("new-project-description-input").value;
  
  const data = new FormData();
  data.append("userId", user_id);
  data.append("title", proj_title)
  data.append("description", proj_discription)
  data.append('image', window.project_create.file)

  fetch('/api/project/', {
    method: "PUT",
    body: data
  }).catch((error) => {
    console.log("Erro creating project: ", error)
  })

  location.reload()
}

async function loadProjectFile(event) {
  window.project_create.file = event.target.files[0];
}
