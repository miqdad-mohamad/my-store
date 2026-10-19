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