function openNav() {
    if (document.getElementById("nav").style.top != "-100%") {
        // original state restoration
        document.getElementById("nav").style.top = "-100%";
        document.getElementById("navshow").style.top = "0px";
        document.getElementById("navshow").style.left = "0px";
        document.getElementById("nav").style.backgroundColor = "#3c3c3fc0";
        document.getElementById("navshow").style.backgroundColor = "#3c3c3fc0";
        document.getElementById("navshow").style.padding = "15px";
        document.getElementById("navshow").style.borderRadius = "0px 0px 18px 0px";
        document.getElementById("navshow").textContent = "=";
    } else {
        // open state
        document.getElementById("nav").style.top = "0px";
        document.getElementById("navshow").style.top = "5px";
        document.getElementById("navshow").style.left = "5px";
        document.getElementById("navshow").style.backgroundColor = "red";
        document.getElementById("nav").style.backgroundColor = "black";
        document.getElementById("navshow").style.padding = "5px 10px 5px 10px";
        document.getElementById("navshow").style.borderRadius = "32px";
        document.getElementById("navshow").textContent = "x";
    }
}