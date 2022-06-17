document.querySelector(".collapsible").addEventListener("click", function () {
    this.classList.toggle("open");
    var content = this.nextElementSibling;
    while (content && content.classList.contains("dataContent")) {
        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }
        content = content.nextElementSibling;
    }
});