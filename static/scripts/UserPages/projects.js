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
  const proj_link = document.getElementById("new-project-title-input").value;
  
  const data = new FormData();
  data.append("userId", user_id);
  data.append("title", proj_title)
  data.append("description", proj_discription)
  data.append('image', window.project_create.file)
  data.append('link', proj_link)

  console.log(data)

  await fetch('/api/project/', {
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

async function loadProjectFile2(event) {    
    const user_id = document.getElementById("user-id-info").value;
    const proj_id = event.srcElement.id.split('-')[1]
    const image_original = document.getElementById(proj_id);
    const image = document.createElement("img");
    image.width = 250;
    image.height = 250;
    image.src = URL.createObjectURL(event.target.files[0]);
    image.id = "person-photo";
    image_original.replaceWith(image);
  
    const data = new FormData()
    data.append("userId", user_id)
    data.append('projId', proj_id)
    data.append('image', event.target.files[0])
  
    fetch('/api/v1/image/project/', {
      method: "PUT",
      body: data
    })
    // // CREATE FETCH REQUEST WITH PROPER URL: "DONT KNOW WHAT THE URL IS"
  }