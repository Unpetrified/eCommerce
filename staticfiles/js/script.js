if (user==='AnonymousUser') {
    updateCart()
    console.log('User not authenticated');
    $('.add-cart-btn').on('click', function (e) {
        e.preventDefault();
        var productId = this.dataset.product;
            action = this.dataset.action;
            
        addToCart(productId, action);
        
    });
} else {
    updateCartIndicator();
    console.log('User is authenticated');
    $('.add-cart-btn').on('click', function (e) {
        e.preventDefault();
        var productId = this.dataset.product;
            action = this.dataset.action;
            
        updateUserOrder(productId, action);
        
    });
}

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
        cart_table.css('display', 'none')
        $('.cart_details').html('<p class="empty-cart">Your cart is empty.</p>')
    } else {
        cart_table.css('display', 'block')
    }
}

function addToCart(productId, action, value = 0) {
    if (action === 'add') {

        if(cart[productId] == undefined) {
            cart[productId] = {'quantity':1};
        } else {
            cart[productId]['quantity'] += 1;
        }

    } else if (action === 'remove') {

        cart[productId]['quantity'] -= 1;
        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId];
        }
    } else if (action === 'view-addition') {
        console.log(value);
        if (value > 0) {
            cart[productId] = {'quantity':value};
        } else if (value <= 0) {
            delete cart[productId];
        }
    }
    setCookie('cart', cart);
    updateCart();
}
