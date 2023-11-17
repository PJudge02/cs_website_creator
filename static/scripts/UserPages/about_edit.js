window.addEventListener("DOMContentLoaded", async () => {
    const save_btn = document.getElementById("info-modal-save-btn")
    save_btn.addEventListener("click", saveAbout)
})

async function saveAbout() {
    const user_id = document.getElementById("user-id-info").value
    const about_info_form = document.getElementById("info-modal-form")
    params = new FormData(about_info_form)
    console.log(params)
}