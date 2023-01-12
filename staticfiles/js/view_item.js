$('.add').on('click', function (e) {

    e.preventDefault();
    var qnty = $('.qnty');

    if (qnty.val() !== "") {
        add_to_cart(e, parseInt(qnty.val()), false);
    }
    
    update_cart_indicator();

    qnty.val("");
});