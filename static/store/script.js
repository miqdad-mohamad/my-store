document.addEventListener('DOMContentLoaded', () => {

    const toggleBtn = document.getElementById('categories-toggle');
    const categoriesList = document.getElementById('categories-list');

    if (toggleBtn && categoriesList) {


        toggleBtn.addEventListener('click', () => {


            categoriesList.classList.toggle('hidden');


            toggleBtn.classList.toggle('active');

        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';

            setTimeout(function () {
                alert.remove();
            }, 500);

        }, 4000);
    });
});