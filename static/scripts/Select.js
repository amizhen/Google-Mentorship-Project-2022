document.querySelector('.selectTrigger').addEventListener('click', function () {
    this.parentElement.classList.toggle('open');
    var optionsWrapper = this.parentElement.querySelector(".selectOptions");
    for (var i = 0; i < optionsWrapper.children.length; i++) {
        var child = optionsWrapper.children[i];
        if (child && child.classList.contains("selectOption")) {
            if (child.style.maxHeight) {
                child.style.maxHeight = null;
                child.style.visibility = "hidden";
            } else {
                child.style.maxHeight = child.scrollHeight + "px";
                child.style.visibility = "visible";
            }
        }
    }
})

function getSelection() {
    return document.querySelector(".selectTrigger span").textContent;
}

function closeSelectionPanel() {
    if (document.querySelector('.select').classList.contains('open')) {
        document.querySelector('.select').classList.toggle('open');
    }
    var optionsWrapper = document.querySelector('.selectOptions');
    for (var i = 0; i < optionsWrapper.children.length; i++) {
        var child = optionsWrapper.children[i];
        child.style.maxHeight = null;
        child.style.visibility = "hidden";
    }
}

for (const option of document.querySelectorAll(".selectOption")) {
    option.addEventListener('click', function () {
        if (!this.classList.contains('selected')) {
            if (this.parentNode.querySelector('.selectOption.selected')) {
                this.parentNode.querySelector('.selectOption.selected').classList.remove('selected');
            }
            this.classList.add('selected');
            this.closest('.select').querySelector('.selectTrigger span').textContent = this.textContent;
        }
        closeSelectionPanel();
    })
}

