const selector = document.getElementById("selector")


function reset() {
    const elements = document.getElementsByClassName("shown")
    for (let i = 0; i < elements.length; i++) {
        elements[i].classList.add("hidden")
        elements[i].classList.remove("shown")
    }
}

selector.addEventListener("change", function (e) {
    reset()
    document.getElementById(e.target.value).classList.toggle("hidden")
    document.getElementById(e.target.value).classList.toggle("shown")
})