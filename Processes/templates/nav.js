function openNav() {
    if (document.getElementById("nav").style.width == "200px") {
        document.getElementById("nav").style.width = "0px";
        document.getElementById("navshow").style.left = "0px";
    } else {
        document.getElementById("nav").style.width = "200px";
        document.getElementById("navshow").style.left = "200px";
    }
}