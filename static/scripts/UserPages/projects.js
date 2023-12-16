window.addEventListener("DOMContentLoaded", async () => {
    const new_proj_btn = document.getElementById("save-new-project-btn");
    new_proj_btn.addEventListener("click", new_proj);
  });

  async function new_lang() {
  const user_id = parseInt(document.getElementById("user-id-info").value);
  const proj_title = document.getElementById("new-project-title-input").value;
  const proj_discription = document.getElementById("new-project-description-input").value;
  const proj_img = document.getElementById("new-project-image-input").value

  const image = document.createElement('img');
  image.width = 150;
  image.height = 150; 

  const values = {};
  values.title = proj_title;
  values.discription = proj_discription;
//   values.img = proj_img
  values.userId = user_id;

  const req = new XMLHttpRequest();
  req.open("PUT", `/api/language/`, true);
  req.setRequestHeader("Content-type", "application/json; charset=utf-8");
  req.send(JSON.stringify(values));

  const lang_list = document.getElementById("language-list");
  const lang_li = document.createElement("li");
  lang_li.classList.add("list-group-item")
  lang_li.innerText = `${lang_name}, ${lange_prof}`;
  lang_list.appendChild(lang_li);
}

async function loadProjectFile(event){
    const icon = document.getElementById("person-photo");
    const image = document.createElement('img');
    image.width =50;
    image.height =50; 
    image.src = URL.createObjectURL(event.target.files[0]);
    image.id="person-photo"
    icon.replaceWith(image);
    // const r = await fetch() 
    //CREATE FETCH REQUEST WITH PROPER URL: "DONT KNOW WHAT THE URL IS"
  }