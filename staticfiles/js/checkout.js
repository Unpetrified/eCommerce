if (user !== 'AnonymousUser') {
    $('.contact').css('display', 'none')
}

$('.shipping-btn').on('click', function (e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).toggle();
    $('.payment-field').toggle();
});

$('.shipping-field').on('click', function (e) {
    e.preventDefault();
    if ($('.shipping-btn').css('display') === 'none') {
        $('.shipping-btn').toggle();
        $('.payment-field').toggle();   
    }
})

$('.make-payment').on('click', function (e) {
    submitForm();
})

function submitForm() {
    var userInfo = {
        'name' : null,
        'phone' : null,
        'total' : total,
    };

    var shippingInfo = {
        'address' : $('#address').val(),
        'city' : $('#city').val(),
        'state' : $('#state').val(),
        'country' : $('#country').val(),
    };

    if (user==='AnonymousUser') {
        userInfo.name = $('#name').val();
        userInfo.phone = $('#number').val();
    }

    fetch(url, {
        method : 'POST',
        headers : {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrf_token
        },
        body : JSON.stringify({'shippingInfo':shippingInfo, 'userInfo':userInfo})
    }).then((res) => {return res.json()})
    .then((data) => {
        console.log(data);
        alert('Transaction complete');
        window.location.href = '/'
    })
}