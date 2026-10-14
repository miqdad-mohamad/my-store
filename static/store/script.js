// ننتظر لحد ما تحمل الصفحة كاملة
document.addEventListener('DOMContentLoaded', () => {
    
    // 1. نمسك العناصر بالـ ID
    const toggleBtn = document.getElementById('categories-toggle');
    const categoriesList = document.getElementById('categories-list');

    // 2. نتأكد إنهم موجودين بالصفحة (عشان ما يطلع خطأ)
    if (toggleBtn && categoriesList) {
        
        // 3. نضيف حدث "الضغط" (Click)
        toggleBtn.addEventListener('click', () => {
            
            // 4. نخفي أو نظهر القائمة
            categoriesList.classList.toggle('hidden');
            
            // 5. نلف السهم
            toggleBtn.classList.toggle('active');
            
        });
    }
});