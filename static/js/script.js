if (user==='AnonymousUser') {
    console.log('User not authenticated');
} else {
    updateCartIndicator('.cart-quantity')
    console.log('User is authenticated');
}

$('.add-cart-btn').on('click', function (e) {
    e.preventDefault();
    var productId = this.dataset.product;
        action = this.dataset.action
    updateUserOrder(productId, action)
});

function updateUserOrder(productId, action, event = false) {
    var url = '/addtocart';
    fetch(url, {
        method : 'POST',
        headers : {
            'Content-Type':'application/json',
            'X-CSRFToken' : csrf_token
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    }, 
    ).then((res) => {
        return res.json()
    }).then((data) => {
        updateCartIndicator('.cart-quantity');
        updateCartIndicator('.items')
        if (event) {
            var qnt = event.target.parentNode.parentNode.children[0];
            qnt.textContent = data;
            if (data === 0) {
                event.target.parentNode.parentNode.parentNode.remove()
            }
        }
    })
}

function updateCartIndicator(path) {
    var url = '/addtocart'
    fetch(url).then((res) => {return res.json()}).then((data) => {
        $(path).text(data);
    })
}