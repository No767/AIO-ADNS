function openNav() {
    if (document.getElementById("nav").style.left != "-100%") {
        // original state restoration
        document.getElementById("nav").style.left = "-100%";
        document.getElementById("navshow").style.left = "0px";
        document.getElementById("navshow").style.top = "0px";
        document.getElementById("navshow").style.backgroundColor = "#3c3c3fc0";
        document.getElementById("navshow").style.padding = "15px";
        document.getElementById("navshow").style.borderRadius = "0px 0px 18px 0px";
        document.getElementById("navshow").textContent = "=";
    } else {
        // open state
        document.getElementById("nav").style.left = "0px";
        document.getElementById("navshow").style.left = "5px";
        document.getElementById("navshow").style.top = "5px";
        document.getElementById("navshow").style.backgroundColor = "red";
        document.getElementById("navshow").style.padding = "0px 5px 0px 5px";
        document.getElementById("navshow").style.borderRadius = "32px";
        document.getElementById("navshow").textContent = "x";
    }
}

function render_nav() {
    document.getElementById('navContainer').innerHTML = `<button id="navshow" onclick="openNav()">=</button>
    <div id="nav" class="nav">
        <ul>
            <li><a href="/"><button>Home</button></a></li>
            <li><a href="/block"><button>Block</button></a></li>
            <li><a href="/route"><button>Route</button></a></li>
            <li><a href="/toggleONOFF"><button>Toggle</button></a></li>
        </ul>
    </div>`;
    openNav();
}