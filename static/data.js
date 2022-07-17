fetch('http://127.0.0.1:5000/tienda/api')

.then(function(response){
    return response.json();
})

.then(function(products){
    let placeholder = document.querySelector("#data-output");
    let out = "";

    for(let product of products){
        out += `
            <tr>
                <td> <img src='${product.img}' class="tamaño"> </td>
                <td class="texto">${product.name}</td>
                <td class="texto">$${product.price}</td>
                <td class="texto">${product.description}</td>
                <td class="texto">${product.owner}</td>
            </tr>
        `;
    }

    placeholder.innerHTML=out;
})