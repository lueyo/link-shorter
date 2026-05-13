
const hostname = "lueyo.es";
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const url = document.querySelector('input[name="url"]').value;
        const password = document.querySelector('input[name="password"]').value;
        const body = { url: url };
        if (password) {
            body.password = password;
        }
        fetch('/s/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        })
        .then(response => {
            if (response.status === 201 || response.status === 200) {
                return response.json().then(data => {
                    short_code = data.short_code;
                    let existingSpan = document.querySelector('body > span');
                    if (existingSpan) {
                        existingSpan.remove();
                    }
                    const span = document.createElement('span');
                    const button = document.createElement('button');
                    button.textContent = '📋';
                    const shortUrl = `https://${hostname}/s/${short_code}`;

                    span.innerHTML = `Created Successfully: <a href="/s/${short_code}" target="_blank">${shortUrl}</a>`;

                    button.addEventListener('click', function() {
                        navigator.clipboard.writeText(shortUrl).then(() => {
                            button.classList.add('copiado');
                            setTimeout(() => {
                                button.classList.remove('copiado');
                            }, 3000);
                        }).catch(err => {
                            console.error('Error in copying URL: ', err);
                        });
                    });
                    span.appendChild(button);
                    document.body.appendChild(span);
                });
            } else {
                let existingSpan = document.querySelector('body > span');
                if (existingSpan) {
                    existingSpan.remove();
                }
                const span = document.createElement('span');
                span.textContent = 'Error';
                document.body.appendChild(span);
                return Promise.reject('Failed to create');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});