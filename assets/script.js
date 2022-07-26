document.querySelector('.no-js').classList.remove('no-js');

[...document.querySelectorAll('time')].forEach((elem) => {
    const date = new Date(elem.dateTime);
    elem.textContent = date.toLocaleString();
});
