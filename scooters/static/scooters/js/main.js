
fetch('http://127.0.0.1:8000/scooters/api/main/')
    .then(response => {
        if(!response.ok){
            throw Error('Could not fetch resource');
        }
        return response.json()
    })
    .then(data => {
        const ul = document.createElement('ul')
        ul.classList.add('scooter')
        data.forEach(function (element){
            const li = document.createElement('li')
            li.innerHTML = `<a href="http://127.0.0.1:8000/scooters/main/${element.id}">${element.brand} ${element.scooter_model}</a>`
            ul.appendChild(li)
            document.body.appendChild(ul)
        });
    })
    .catch(error => console.error(error));
