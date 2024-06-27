function getEmail() {
    return fetch("/GetEmail",).then((response) =>
        response.json()).then((data) => {
            // console.log(data);
            return data;
        }
    );
}

const email = getEmail().then((email) => {

    if (email) {
        document.getElementById("login").style.display = "none";
        document.getElementById("logout").style.display = "block";
        document.getElementById("outData").textContent = email.split("@")[0];
    }

});
