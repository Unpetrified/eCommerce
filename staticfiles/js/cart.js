if (user==='AnonymousUser') {
    checkEmptyCart(Object.keys(cart).length);
}

$('.increase').on('click', function (e) {
    var productId = this.dataset.product;
        action = this.dataset.action;
    if (user==='AnonymousUser') {
        addToCart(productId, action, e);
    } else {
        updateUserOrder(productId, action, e);
    }
});

$('.decrease').on('click', function (e) {
    var productId = this.dataset.product;
        action = this.dataset.action;
    if (user==='AnonymousUser') {
        addToCart(productId, action, e);
    } else {
        updateUserOrder(productId, action, e);
    }
});