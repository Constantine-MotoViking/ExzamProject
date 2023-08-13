$(document).ready(() => {
    let correct1 = false;
    let correct2 = true;
    let correct3 = false;
    let correct4 = true;

    let regExp1 = /^[a-zA-Z]{1}[a-zA-Z0-9_\-]{5,15}$/;
    let regExp2 = /^...$/;
    let regExp3 = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    $('#login').blur(() => {
        let loginX = $('#login').val();
        if (regExp1.test(loginX)) {
            $.ajax({
                url: '/accounts/ajax_reg',
                data: { login: loginX },
                success: function(response) {
                    if (response.login_message === 'зайнятий') {
                        $('#login-mess').text('Логін зайнятий! Спробуйте інший!');
                        correct1 = false;
                    } else {
                        $('#login-mess').text('');
                        correct1 = true;
                    }
                }
            });
        } else {
            correct1 = false;
            $('#login-mess').text('Логін не відповідає вимогам безпеки!');
        }
    });

    $('#email').blur(() => {
        let emailX = $('#email').val();
        if (regExp3.test(emailX)) {
            $.ajax({
                url: '/accounts/ajax_reg',
                data: { email: emailX },
                success: function(response) {
                    if (response.email_message === 'зайнятий') {
                        $('#email-mess').text('E-Mail зайнятий! Спробуйте інший!');
                        correct3 = false;
                    } else {
                        $('#email-mess').text('');
                        correct3 = true;
                    }
                }
            });
        } else {
            correct3 = false;
            $('#email-mess').text('Некоректний формат E-Mail!');
        }
    });

    $('#submit').click(() => {
        if (correct1 && correct2 && correct3 && correct4) {
            $('#form1').attr('onsubmit', 'return true');
        } else {
            $('#form1').attr('onsubmit', 'return false');
            alert('Форма містить некоректні дані! \nВідправка даних заблокована!');
        }
    });
});
