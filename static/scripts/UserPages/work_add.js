window.addEventListener("DOMContentLoaded", async () => {
  const new_lang_btn = document.getElementById("save-new-work-btn");
  new_lang_btn.addEventListener("click", new_work);
});

async function new_work() {
  const user_id = parseInt(document.getElementById("user-id-info").value);
  const title = document.getElementById("work-title-input").value;
  const workplace = document.getElementById("work-workplace-input").value;
  const description = document.getElementById("work-description-input").value;
  const startYear = document.getElementById("work-from-input").value;
  const endYear = document.getElementById("work-to-input").value;

  const values = {};
  values.userId = user_id;
  values.title = title;
  values.workplace = workplace;
  values.description = description;
  values.startYear = startYear;
  values.endYear = endYear;

  const workId = await fetch(`/api/work/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(values),
  }).then(validateJSON)
  .catch((error) => {
    console.log("Error Creating Language Data: ", error);
  });

  const work_list = document.getElementById("work-list");
  const work_li = document.createElement("li");
  work_li.classList.add("list-group-item","drag-item");
  work_li.draggable = true
  work_li.id = `work-li-${workId.id}`
  
  const work_icon = document.createElement("i");
  work_icon.classList.add("fa-solid", "fa-briefcase");
  const work_name = document.createElement("p");
  work_name.innerText = ` ${title}, ${workplace} ${startYear}-${endYear}`;

  work_li.appendChild(work_icon);
  work_li.innerHTML += work_name.innerText;

  const work_desc = document.createElement("p");
  work_desc.innerText = description;
  work_li.appendChild(work_desc);
  work_list.appendChild(work_li);
}
