var $qnty = $('.cart-quantity');

// get or set the cart value
if (JSON.parse(localStorage.getItem("cart"))) {
    var cart = JSON.parse(localStorage.getItem("cart"));
} else {
    var cart = {}
}

update_cart_indicator();

$('.add-cart-btn').on('click', function (e) {
    e.preventDefault();
    add_to_cart(e);
    update_cart_indicator();
});

function add_to_cart(event, qty=1, source=true) {
    var img_src = $(event.target.parentNode.parentNode.children[0]).attr('src');
    var price = parseFloat($(event.target.parentNode.children[2]).text());
    var name = $(event.target.parentNode.parentNode.children[1]).text();

    if (qty === 0) {
        console.log('zero given');
    } else {

        if (cart[name]) {
            if (source) {
                cart[name][2] += qty;
            } else {
                cart[name][2] = qty;
                source = true;
            }
        } else {
            cart[name] = [img_src, price, qty]
        }

    }
    
    localStorage.setItem("cart", JSON.stringify(cart));
}

function update_cart_indicator() {
    $qnty.css('display', 'inline');
    var items = Object.keys(cart).length;
    $qnty.text(items);
}