function CartUpdate() {
    let t_href = event.target.getAttribute('href');
    var href =  $(this).data("href");
    var seller_id = $(this).data("seller");
    var product_id = $(this).data("product");
    console.log(href)
        $.ajax(
            {
                url: href,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: window.CSRF_TOKEN,
                    seller_id: seller_id,
                    product_id: product_id
                },
                success: function (data){
                    console.log(data.items)
                    $(".CartBlock-amount").text(data['cart_count']);
                    $(".CartBlock-price").text(data['cart_sum']);

                    $('.Cart').html(data.items)
                }
            }
        )
}

$(document).ready(function(){
    $('.Cart').on('click', 'button[type="button"]', CartUpdate)


}
)
function AddToCart(url, product, seller) {
    var value=document.getElementById('amount');
    if (value != null) {
        count=value.value;
    } else { count=1; }
    $.ajax({
        url: url,
        type: "POST",
        data: {
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            seller_id: seller,
            product_id: product,
            count: count
        },

        success: (data) => {
            $("#modal_open").fadeIn(200);

            $(".CartBlock-amount").text(data['cart_count']);
            $(".CartBlock-price").text(data['cart_sum']);

            },

  });
}

$("body").click(function () {
    $("#modal_open").fadeOut(300);
});

$(".close").click(function () {
    $("#modal_open").fadeOut(300);
});
