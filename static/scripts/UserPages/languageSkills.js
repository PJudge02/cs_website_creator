window.addEventListener("DOMContentLoaded", async () => {
  const new_lang_btn = document.getElementById("save-new-lang-btn");
  new_lang_btn.addEventListener("click", new_lang);
});

async function new_lang() {
  const user_id = parseInt(document.getElementById("user-id-info").value);
  const lang_name = document.getElementById("new-language-input").value;
  const lange_prof = document.getElementById("new-proficiency-input").value;

  const values = {};
  values.name = lang_name;
  values.proficiency = lange_prof;
  values.userId = user_id;

  const langId = await fetch(`/api/language/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(values),
  }).then(validateJSON)
  .catch((error) => {
    console.log("Error Creating Language Data: ", error);
  });

  const lang_list = document.getElementById("language-list");
  const lang_li = document.createElement("li");
  lang_li.classList.add("list-group-item", "drag-item");
  lang_li.draggable = true
  lang_li.id = `lang-li-${langId.id}`
  lang_li.innerText = `${lang_name}, ${lange_prof}`;
  lang_list.appendChild(lang_li);
}
