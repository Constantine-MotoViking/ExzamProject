$(document).ready(() => {

    console.log('shop.js -> Start');
    $('#catalog-panel').on('click', '#add-to-cart', (event) => {
        // 1
        console.log('add-btn -> Click');

        //2
        const userId =$('#user-id').val();
        console.log('userId -> ' + userId);

        // 3
        if (userId == 'None') {
            alert('Для використання кошику Ви повинні авторизуватись!');
            // -> goto signin.html
        } else {
            // 4
            let productId = $(event.target).prev().val();
            console.log('productId -> ' + productId);

            //5
            const productPriceText = $(event.target).closest('.product-description').find('.product-price').text();
            // Видаліть символи долара та пробіли
            const cleanedPriceText = productPriceText.replace(/\$/g, '').trim();
            // Перетворіть текст ціни у числовий формат
            const productPrice = parseFloat(cleanedPriceText);
            console.log('productPrice -> ' + productPrice);

            const productImageURL = $(event.target).closest('.single-product-wrapper').find('.product-img img').attr('src');

            // AJAX-запит на збереження товару у бд:
            $.ajax({
                url: '/bill/ajax_cart',
                data: `uid=${userId}&pid=${productId}&price=${productPrice}`,
                success: (response) => {
                    console.log('AJAX -> OK / ' + response.message);
                    alert('Товар успішно доданий до кошика');
                    $('#count').text(response.count);
                    $('#_count').text(`Товарів у кошику: ${response.count} шт`);
                    $('#_amount').text(`Загальна вартість: ${response.amount} грн`);
                }
            });
        }
    });
});
