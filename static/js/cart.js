var total = 0,
    items = 0,
    cart = JSON.parse(localStorage.getItem("cart")),
    cartList = Object.keys(cart);
$('document').ready(function(e) {
    var cartItems = $('tbody');

    // populate the rundown of the items in cart
    for (var i = 0; i < cartList.length; i++) {
        var newRow = '<tr>';
        newRow += '<td><img src="'+ cart[cartList[i]][0] +'" alt="" class="image"></td>';
        newRow += '<td>'+ cartList[i] +'</td>';
        newRow += '<td>'+ cart[cartList[i]][1] +'</td>';
        newRow += '<td class="quantity"><span>'+ cart[cartList[i]][2] +'</span><span class="increase-decrease"><span class="increase"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><!--! Font Awesome Free 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2022 Fonticons, Inc. --><path d="M361 215C375.3 223.8 384 239.3 384 256C384 272.7 375.3 288.2 361 296.1L73.03 472.1C58.21 482 39.66 482.4 24.52 473.9C9.377 465.4 0 449.4 0 432V80C0 62.64 9.377 46.63 24.52 38.13C39.66 29.64 58.21 29.99 73.03 39.04L361 215z"/></svg></span><span class="decrease"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><!--! Font Awesome Free 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2022 Fonticons, Inc. --><path d="M361 215C375.3 223.8 384 239.3 384 256C384 272.7 375.3 288.2 361 296.1L73.03 472.1C58.21 482 39.66 482.4 24.52 473.9C9.377 465.4 0 449.4 0 432V80C0 62.64 9.377 46.63 24.52 38.13C39.66 29.64 58.21 29.99 73.03 39.04L361 215z"/></svg></span></span></td>'
        newRow += '<td>'+ get_total(cartList[i]) +'</td>';
        newRow += '<td class="remove"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Free 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2022 Fonticons, Inc. --><path d="M135.2 17.69C140.6 6.848 151.7 0 163.8 0H284.2C296.3 0 307.4 6.848 312.8 17.69L320 32H416C433.7 32 448 46.33 448 64C448 81.67 433.7 96 416 96H32C14.33 96 0 81.67 0 64C0 46.33 14.33 32 32 32H128L135.2 17.69zM394.8 466.1C393.2 492.3 372.3 512 346.9 512H101.1C75.75 512 54.77 492.3 53.19 466.1L31.1 128H416L394.8 466.1z"/></svg></td></tr>';
        cartItems.append(newRow);
        total += get_total(cartList[i]);
        items += 1;
    }

    $('.remove').on('click', function (e) {
        var cartTotal = $('.total'),
            itemTotal = e.target.parentNode.children[4].textContent;
        cartTotal.text(eval(cartTotal.text() +'-'+itemTotal).toFixed(2));
        delete_item(e.target.parentNode);
            
    });

    $('.total').text(total.toFixed(2));
    $('.items').text(items);

    $('.increase').on('click', function(e) {
       
        update_item_and_total(e, "+");

    });
    
    $('.decrease').on('click', function(e) {
        
        update_item_and_total(e, "-");

    });

});

empty();

function update_item_and_total(e, sign) {

    var itemTotal = e.target.parentNode.parentNode.parentNode.children[4],
    quantity = e.target.parentNode.parentNode.children[0].textContent;

    var cartTotal = $('.total'),
        oldCartTotal = cartTotal.text(),
        oldItemTotal = itemTotal.textContent;

    // update item quantity in DOM and Cart
    if (sign === "+") {
        quantity = eval(quantity + "+1");
    } else if (sign === "-") {
        quantity = eval(quantity + "-1");
    }

    $(e.target.parentNode.parentNode.children[0]).text(quantity);
    var itemName = e.target.parentNode.parentNode.parentNode.children[1].textContent;
    cart[itemName][2] = quantity;

    // update item total in DOM
    itemTotal.textContent = get_total(itemName).toFixed(2);

    var newItemTotal = itemTotal.textContent;

    // update cart total
    cartTotal.text(eval(oldCartTotal +'-'+oldItemTotal +'+'+newItemTotal).toFixed(2));

    if (sign ==="-" && quantity === 0) {
        delete_item(e.target.parentNode.parentNode.parentNode);
    }
    // save cart 
    localStorage.setItem("cart", JSON.stringify(cart));
}

function empty () {
    if (Object.keys(cart).length === 0) {
        $(".display-cart").html("<p class='empty'>Empty Cart</p>");
        $(".checkout").css("display", "none")
    }
}

function get_total(item) {
    var total = eval(cart[item][2]+"*"+cart[item][1]);
    return total.toFixed(2)
};

function delete_item(row, dict=cart) {
    key = row.children[1].textContent;
    if (dict.hasOwnProperty(key)) {
        delete dict[key];
        var items = $('.items'),
            itemTotal = items.text();
        items.text(eval(itemTotal+'-1'));
        row.remove();
        update_cart_indicator();
        empty();
        localStorage.setItem("cart", JSON.stringify(cart));
        return
    }
}