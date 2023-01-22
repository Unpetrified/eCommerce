$('.increase').on('click', function (e) {
    var productId = this.dataset.product;
        action = this.dataset.action
    updateUserOrder(productId, action, e)
});

$('.decrease').on('click', function (e) {
    var productId = this.dataset.product;
        action = this.dataset.action
    updateUserOrder(productId, action, e)
});
