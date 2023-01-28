$('.add').on('click', function (e) {

    e.preventDefault();
    var qnty = $('input');

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

});