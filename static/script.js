
const hostname = location.hostname;
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
        const url = document.querySelector('input[name="url"]').value;
        fetch('/s/', { // Changed the fetch URL to '/s/'
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }), // Send the data as JSON
        })
        .then(response => {
            console.log(response); // Log the raw response
            if (response.status === 201 || response.status === 200) {
                return response.json().then(data => {
                    console.log(data); // Log the parsed JSON
                    short_code = data.short_code;
                    // obtain the short_code from the data object and display it
                    console.log(short_code);

                    let existingSpan = document.querySelector('body > span');
                    if (existingSpan) {
                        existingSpan.remove();
                    }
                    // Assuming short_code and hostname are defined and contain the necessary values
                    const span = document.createElement('span');
                    const button = document.createElement('button');
                    button.textContent = '📋';
                    const url = `https://${hostname}/s/${short_code}`;

                    span.innerHTML = `Created Successfully: <a href="/s/${short_code}" target="_blank">${url}</a>`;

                    // Event listener for the button
                    button.addEventListener('click', function() {
                        navigator.clipboard.writeText(url).then(() => {
                            console.log('URL copied to clipboard');
                            button.classList.add('copiado'); // Añade la clase .copiado al botón
                            setTimeout(() => {
                                button.classList.remove('copiado'); // Quita la clase .copiado después de 3 segundos
                            }, 3000); // 3000 milisegundos = 3 segundos
                        }).catch(err => {
                            console.error('Error in copying URL: ', err);
                        });
                    });
                    // Append the button to the span
                    span.appendChild(button);

                    
                    document.body.appendChild(span);
                    console.log(data);
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