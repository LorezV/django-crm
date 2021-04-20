let inputActiveElem

window.onload = function() {
    let inputSet = document.getElementsByClassName('input-disabled')
    let createOrderButton = document.getElementById('order_create_href_id')
    let createOrderForm = document.getElementById('order_create_form_id')

    if (createOrderButton != undefined) {
        createOrderButton.addEventListener('click', function(event) {
            createOrderForm.classList.toggle('active')
        })
    }

    for (let i = 0; i < inputSet.length; i++) {
        let elem = inputSet[i]

        //Read-only making and add events on inputs
        disableInput(elem)
        elem.addEventListener('dblclick', function (event) {
            enableInput(elem)
            console.log(event)
        })
    }
    // Read-only disable by click on page
    document.addEventListener('mousedown', function(event) {
        if (inputActiveElem != undefined && event.target != inputActiveElem) {
            disableInput(inputActiveElem)
        }
    })
}

function disableInput(elem) {
    elem.setAttribute('readonly', '')
}

function enableInput(elem) {
    if (inputActiveElem != undefined) {
        disableInput(inputActiveElem)
    }
    elem.removeAttribute("readonly")
    elem.focus()
    inputActiveElem = elem
}