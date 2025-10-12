let selectedSize = null;

function selectSize(element) {
    // Убираем выделение у всех размеров
    const allSizes = document.querySelectorAll('.size-option');
    allSizes.forEach(size => {
        size.classList.remove('border-black', 'bg-black', 'text-white');
        size.classList.add('border-gray-200', 'text-black', 'hover:border-black', 'hover:bg-gray-50');
    });

    // Добавляем выделение выбранному размеру
    element.classList.remove('border-gray-200', 'text-black', 'hover:border-black', 'hover:bg-gray-50');
    element.classList.add('border-black', 'bg-black', 'text-white');
    selectedSize = element;

    // Сохраняем выбранный размер в скрытом поле
    document.getElementById('selected-size').value = element.dataset.sizeId;
}

function changeMainImage(src, clickedElement) {
    // Меняем главное изображение
    const mainImg = document.getElementById('main-product-image');
    if (mainImg) {
        mainImg.src = src;
    }

    // Убираем класс active у всех миниатюр
    const allThumbnails = document.querySelectorAll('.product-thumbnail');
    allThumbnails.forEach(thumb => {
        thumb.classList.remove('border-black');
        thumb.classList.add('border-gray-200');
    });

    // Добавляем класс active к нажатой миниатюре
    clickedElement.classList.remove('border-gray-200');
    clickedElement.classList.add('border-black');
}