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
                    const existingResult = document.querySelector('.result');
                    if (existingResult) {
                        existingResult.remove();
                    }
                    const shortUrl = `https://${hostname}/s/${short_code}`;

                    const resultDiv = document.createElement('div');
                    resultDiv.className = 'result';

                    const urlSpan = document.createElement('div');
                    urlSpan.className = 'result-url';
                    urlSpan.textContent = shortUrl;

                    const copyBtn = document.createElement('button');
                    copyBtn.className = 'btn-copy';
                    copyBtn.textContent = 'Copiar';

                    copyBtn.addEventListener('click', function() {
                        navigator.clipboard.writeText(shortUrl).then(() => {
                            copyBtn.classList.add('copied');
                            copyBtn.textContent = '✓ Copiado';
                            setTimeout(() => {
                                copyBtn.classList.remove('copied');
                                copyBtn.textContent = 'Copiar';
                            }, 3000);
                        }).catch(err => {
                            console.error('Error in copying URL: ', err);
                        });
                    });

                    resultDiv.appendChild(urlSpan);
                    resultDiv.appendChild(copyBtn);
                    document.querySelector('.card').appendChild(resultDiv);
                });
            } else {
                const existingResult = document.querySelector('.result');
                if (existingResult) {
                    existingResult.remove();
                }
                const resultDiv = document.createElement('div');
                resultDiv.className = 'result';
                resultDiv.style.background = 'rgba(239, 68, 68, 0.1)';
                    resultDiv.style.border = '1px solid rgba(239, 68, 68, 0.2)';
                resultDiv.textContent = 'Error al crear el enlace';
                document.querySelector('.card').appendChild(resultDiv);
                return Promise.reject('Failed to create');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});