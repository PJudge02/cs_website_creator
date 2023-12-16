window.addEventListener("DOMContentLoaded", async () => {
    const new_proj_btn = document.getElementById("save-new-project-btn");
    new_proj_btn.addEventListener("click", new_proj);
  });

async function new_proj() {
    console.log("-----------------------23423434rf23wr23----------------------------");
    const user_id = parseInt(document.getElementById("user-id-info").value);
    const proj_title = document.getElementById("new-project-title-input").value;
    const proj_discription = document.getElementById("new-project-description-input").value;
    const proj_img = document.getElementById("new-project-image-input").value
    console.log(proj_img)

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
    console.log("1HERE!!!!!!!!!!!!")


    // ... (your existing code)

const proj_list = document.getElementById("project-list");
const rDiv = document.createElement("div");
rDiv.classList.add("row");

const colDiv1 = document.createElement("div");
colDiv1.classList.add("col-md-4");

const img = document.createElement("img");
img.classList.add("card-img-top");
img.src = "https://i.ytimg.com/vi/oDPhsO2lspA/maxresdefault.jpg";
img.style.width = "300px";
img.style.height = "200px";
img.alt = "Card image cap";


colDiv1.appendChild(img);

const colDiv2 = document.createElement("div");
colDiv2.classList.add("col-md-4");


const cardBodyDiv = document.createElement("div");
cardBodyDiv.classList.add("card-body");


const cardTitle = document.createElement("h5");
cardTitle.classList.add("card-title");
cardTitle.textContent = proj_title;


const cardText = document.createElement("p");
cardText.classList.add("card-text");
cardText.textContent = proj_discription;
console.log("2HERE!!!!!!!!!!!!")

const tryItOutLink = document.createElement("a");
tryItOutLink.href = "#";  // Update with the correct link
tryItOutLink.classList.add("btn", "btn-primary");
tryItOutLink.textContent = "Try it out";
console.log("3HERE!!!!!!!!!!!!")


// const editButton = document.createElement("button");
// editButton.id = `project-${user_id}-${project_id+1}`;  // Update with the correct project_id
// editButton.type = "button";
// editButton.classList.add("btn");
// editButton.setAttribute("data-bs-toggle", "modal");
// editButton.setAttribute("data-bs-target", "#project-modal");
// console.log("4HERE!!!!!!!!!!!!")


// const editIcon = document.createElement("img");
// editIcon.src = "/static/images/pencil.png";
// editIcon.alt = "Image";
// editIcon.style.width = "20px";
// editIcon.style.height = "20px";
// editIcon.classList.add("rounded-circle");


// editButton.appendChild(editIcon);

cardBodyDiv.appendChild(cardTitle);
cardBodyDiv.appendChild(cardText);
cardBodyDiv.appendChild(tryItOutLink);
// cardBodyDiv.appendChild(editButton);

colDiv2.appendChild(cardBodyDiv);

rDiv.appendChild(colDiv1);
rDiv.appendChild(colDiv2);

proj_list.appendChild(rDiv);
console.log("5HERE!!!!!!!!!!!!")




// ... (your existing code)
}

async function loadProjectFile(event){
    // const icon = document.getElementById("person-photo");
    const image = document.createElement('img');
    image.width =50;
    image.height =50; 
    image.src = URL.createObjectURL(event.target.files[0]);
    // icon.replaceWith(image);

    const data = new FormData()
    data.append("userId", user_id)
    data.append("projId", projId)//------------DOES NOT EXIST
    data.append('image', event.target.files[0])

    fetch('/api/v1/image/profile/', {
        method: "PUT",
        body: data
    })
    // const r = await fetch() 
    //CREATE FETCH REQUEST WITH PROPER URL: "DONT KNOW WHAT THE URL IS"
  }