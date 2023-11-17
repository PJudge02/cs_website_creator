window.addEventListener("DOMContentLoaded", async () => {
    const user_id = document.getElementById("user-id-info").value
    const about_modal_btn = document.getElementById(`about-${user_id}`)
    about_modal_btn.addEventListener("click", loadAboutInfo)
    const save_btn = document.getElementById("info-modal-save-btn")
    save_btn.addEventListener("click", saveAbout)
})

async function loadAboutInfo() {
    const user_name = document.getElementById("user-name").innerText
    const user_about = document.getElementById("user-about").innerText.trim()
    const user_college_major = document.getElementById("user-college-major").innerText
    const user_phone = document.getElementById("user-phone").innerText.trim()

    const nameSplit = user_name.split(" ")
    const firstName = nameSplit[2].trim()
    const lastName = nameSplit[3]
    const college_major = user_college_major.split(", ")
    console.log(college_major)
    const college = college_major[1]
    const major = college_major[0]

    document.getElementById("first-name-input").value = firstName
    document.getElementById("last-name-input").value = lastName
    document.getElementById("description-input").value = user_about
    document.getElementById("university-input").value = college
    document.getElementById("major-input").value = major
    document.getElementById("phone-input").value = user_phone
}

async function saveAbout() {
    const user_id = document.getElementById("user-id-info").value
    const firstName = document.getElementById("first-name-input").value
    const lastName = document.getElementById("last-name-input").value
    const description = document.getElementById("description-input").value
    const college = document.getElementById("university-input").value
    const major = document.getElementById("major-input").value
    const phone = document.getElementById("phone-input").value

    const values = {
        "firstName":firstName,
        "lastName":lastName,
        "description":description,
        "college":college,
        "major":major,
        "phone":phone
    }

    const req = new XMLHttpRequest()
    req.open("PUT", `/api/about/${user_id}/`, true)
    req.setRequestHeader('Content-type','application/json; charset=utf-8');
    req.send(JSON.stringify(values))

    document.getElementById("user-name").innerHTML = `<i class="fa fa-user"></i> About ${firstName} ${lastName}`
    document.getElementById("user-about").innerHTML = '<i class="fa-solid fa-circle-info"></i> ' + description
    document.getElementById("user-college-major").innerHTML = `<i class="fa fa-university"></i> ${major}, ${college}`
    document.getElementById("user-phone").innerHTML = `<a href="tel:${phone}"> <i class="fa-solid fa-phone"></i> ${phone}`
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