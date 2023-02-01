$('.add').on('click', function (e) {
    e.preventDefault();
    var qnty = $('input');
    if (user==='AnonymousUser') {
        var product = this.dataset.product,
            action = this.dataset.action;
        addToCart(product, action, parseInt(qnty.val()));
    } else {
        fetch(url, {
            method : 'POST',
            headers : {
                'Content-Type' : 'application/json',
                'X-CSRFToken' : csrf_token
            },
            body : qnty.val()
        }).then((res) => {
            return res.json();
        }).then((data) => {
            alert(data);
            updateCartIndicator();
        })
    }
    qnty.val('');
});