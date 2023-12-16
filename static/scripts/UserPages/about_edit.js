window.addEventListener("DOMContentLoaded", async () => {
  const about = document.getElementById("about-field-about");
  const college = document.getElementById("about-field-college");
  const major = document.getElementById("about-field-major");
  const phone = document.getElementById("about-field-phone");

  // Options for the observer (which mutations to observe)
  const config = { attributes: true, childList: true, subtree: true };

  // Callback function to execute when mutations are observed
  const callback = (mutationList, observer) => {
    for (const mutation of mutationList) {
      if (mutation.type === "childList") {
        console.log("A child node has been added or removed.");
      } else if (mutation.type === "attributes") {
        saveAbout();
      }
    }
  };

  // Create an observer instance linked to the callback function
  const observer = new MutationObserver(callback);

  // Start observing the target node for configured mutations
  observer.observe(about, config);
  observer.observe(college, config);
  observer.observe(major, config);
  observer.observe(phone, config);
});

async function loadFile(event) {
  console.log(event)
  const user_id = document.getElementById("user-id-info").value;
  const icon = document.getElementById("person-photo");
  const image = document.createElement("img");
  image.width = 250;
  image.height = 250;
  image.src = URL.createObjectURL(event.target.files[0]);
  image.id = "person-photo";
  icon.replaceWith(image);

  const data = new FormData()
  data.append("userId", user_id)
  data.append('image', event.target.files[0])

  fetch('/api/v1/image/profile/', {
    method: "PUT",
    body: data
  })
  //CREATE FETCH REQUEST WITH PROPER URL: "DONT KNOW WHAT THE URL IS"
}

async function saveAbout() {
  const user_id = document.getElementById("user-id-info").value;
  const description = document.getElementById("about-field-about").innerText;
  const college = document.getElementById("about-field-college").innerText;
  const major = document.getElementById("about-field-major").innerText;
  const phone = document.getElementById("about-field-phone").innerText;

  const values = {
    description: description,
    college: college,
    major: major,
    phone: phone,
  };

  fetch(`/api/about/${user_id}/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(values),
  });
}
