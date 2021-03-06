function collapsibleClickHandler() {
    this.classList.toggle("open");
    var content = this.nextElementSibling;
    while (content && content.classList.contains("dataContent")) {
        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }

        setTimeout((content) => {
            if (content.parentNode.classList.contains('dataContent')) {
                content.parentNode.style.maxHeight = content.parentNode.scrollHeight + "px";
            }
        }, 250, content)

        content = content.nextElementSibling;
    }
}

function addEventListenersToCollapsibles() {
    for (const collapsible of document.querySelectorAll('.collapsible')) {
        collapsible.addEventListener('click', collapsibleClickHandler, false);
        collapsible.addEventListener('click', collapsibleClickHandler);
    }

    for (const container of document.querySelectorAll(".dataContent > .dataContent")) {
        container.addEventListener('click', function () {
            if (!this.classList.contains('selected')) {
                for (const selected of document.querySelectorAll('.dataContent > .dataContent.selected')) {
                    selected.classList.remove('selected');
                }
                this.classList.add('selected');
                blackoutIndex = +this.id.substring(9);
                generateGraph();
            }
        });
    }
}

addEventListenersToCollapsibles();