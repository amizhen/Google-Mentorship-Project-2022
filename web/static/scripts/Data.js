var coll = document.getElementsByClassName("collapsible");
for (var i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("collapsibleActive");
        var content = this.nextElementSibling;
        while (content && content.classList.contains("dataContent")) {
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
                console.log("Hi");
            }
            content = content.nextElementSibling;
        }
    });
}