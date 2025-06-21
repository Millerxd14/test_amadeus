document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorContainer = document.getElementById('error-message');

    // Check localStorage for an existing token
    const existingToken = localStorage.getItem('accessToken');
    if (existingToken) {
        // verify variable kind in the localStorage
        console.log('Token found in localStorage:', existingToken);
        const kind = localStorage.getItem('kind');
        if (kind === 'student') {
            // Redirect to admin dashboard or protected page
            window.location.href = '/static/student/index.html'; // Example redirect
        } else if (kind === 'teacher') {
            // Redirect to user dashboard or protected page
            console.log('Kind found in localStorage:', kind);
            window.location.href = '/static/teacher/index.html'; // Example redirect
        } else {
            console.warn('Unknown kind:', kind);
        }
    }


    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            errorContainer.textContent = ''; // Clear previous errors

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            // FastAPI expects form data for OAuth2PasswordRequestForm
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            try {
                const response = await fetch('/auth/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: formData,
                });

                if (response.ok) {
                    const data = await response.json();
                    localStorage.setItem('accessToken', data.access_token);
                    localStorage.setItem('kind', data.kind);
                    // Redirect to a protected page or update the UI
                    if (data.kind === 'student') {
                        window.location.href = '/static/student/index.html'; // Example redirect
                    }
                    else if (data.kind === 'teacher') {
                        window.location.href = '/static/teacher/index.html'; // Example redirect
                    }
                } else {
                    const errorData = await response.json();
                    const message = (errorData.detail || 'Error de autenticación. Por favor, inténtalo de nuevo.');
                    errorContainer.textContent = message;
                }
            } catch (error) {
                console.error('Error:', error);
                errorContainer.textContent = 'Ocurrió un error al intentar iniciar sesión.';
            }
        });
    }
});
