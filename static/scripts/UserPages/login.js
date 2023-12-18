    document.addEventListener('DOMContentLoaded', function() {
        var flashMessage = document.getElementById('flash-message');
        var message = 'Email or Password is incorrect';  // Fetch the first flashed message

        if (message) {
            flashMessage.innerHTML = message;
            flashMessage.style.display = 'block';

            // Hide flash message after 2 seconds
            setTimeout(function() {
                flashMessage.style.display = 'none';
            }, 2000);
        }
    });
