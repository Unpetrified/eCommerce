if (user==='AnonymousUser') {
    console.log('User not authenticated');
} else {
    updateCartIndicator();
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
        updateCartIndicator();
        updateCartIndicator('.items')
    if (event) {
            var qnt = event.target.parentNode.parentNode.children[0],
                item_total = event.target.parentNode.parentNode.parentNode.children[4];
            data = JSON.parse(data);
            if (data['item_qnty'] === 0) {
                event.target.parentNode.parentNode.parentNode.remove();
                return
            }
            qnt.textContent = data['item_qnty'];
            item_total.textContent = data['item_total'];
        }
    })
}

function updateCartIndicator(quantity = '.cart-quantity', total='.total') {
    var url = '/addtocart';
    fetch(url).then((res) => {return res.json()}).then((data) => {
        data = JSON.parse(data);
        $(quantity).text(data['items']);
        $(total).text(data['total']);
        checkEmptyCart(data['items']);
    });
}

function checkEmptyCart(val) {
    var cart_table = $('.display-cart');
    if (val == 0) {
        console.log('Cart is empty');
        cart_table.css('display', 'none')
        $('.cart_details').html('<p class="empty-cart">Your cart is empty.</p>')
    } else {
        console.log('Items are in cart');
        cart_table.css('display', 'block')
    }
}