window.addEventListener("DOMContentLoaded", async () => {
    const save_btn = document.getElementById("info-modal-save-btn")
    save_btn.addEventListener("click", saveAbout)
})

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