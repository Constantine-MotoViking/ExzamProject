$(document).ready(() => {
    console.log('wish.js -> Start');

    $('#catalog-panel').on('click', '#add-to-wish', (event) => {
        // 1
        console.log('add-to-wish-btn -> Click');

        // 2
        const userId = $('#user-id').val();
        console.log('userId -> ' + userId);

        // Отримати pid і price з поточного продукту
        const productId = $(event.target).closest('.single-product-wrapper').find('input[type="hidden"]').val();
        const productPriceText = $(event.target).closest('.single-product-wrapper').find('.product-price').text();
        const productPrice = parseFloat(productPriceText.replace(/\$/g, '').trim());

        // Викликати функцію для перевірки стану товару в обраному на сервері
        $.ajax({
            type: 'GET',
            url: '/bill/check_wishlist',
            data: {
                user_id: userId,
                product_id: productId
            },
            success: (response) => {
                console.log('AJAX -> OK');
                if (response.is_in_wishlist) {
                    // Товар вже в обраному, отже, видаляємо його
                    $.ajax({
                        type: 'POST',
                        url: '/bill/remove_from_wishlist',
                        data: {
                            user_id: userId,
                            product_id: productId
                        },
                        success: (removeResponse) => {
                            console.log('Remove from wishlist -> OK');
                            alert('Товар видалено з обраного');
                            // Оновити лічильник після видалення
                            $('#wish-count').text(removeResponse.count);
                        }
                    });
                } else {
                    // Товар не в обраному, отже, додаємо його
                    $.ajax({
                        url: '/bill/ajax_wish',
                        data: {
                            uid: userId,
                            pid: productId,
                            price: productPrice
                        },
                        success: (response) => {
                            console.log('AJAX -> OK / ' + response.message);
                            alert('Товар успішно доданий до списку бажань');
                            // Оновити лічильник після додавання
                            $('#wish-count').text(response.count);
                        }
                    });
                }
            }
        });
    });
});
