function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

if (!getCookie('cookie_accept')){
const modal = document.querySelector("#modalCookie")
modal.classList.add('active')
}

const acceptBtn = document.querySelector('#acceptCookie')
acceptBtn.addEventListener('click', () => {
    const modal = document.querySelector("#modalCookie")
    modal.classList.remove('active')
    const date = new Date()
    date.setTime(date.getTime() + (10 * 24 * 60 * 60 * 1000))
    document.cookie = `cookie_accept=true; expires=${date.toUTCString()} `;
})

