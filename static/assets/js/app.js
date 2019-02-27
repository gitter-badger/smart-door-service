function search_logs()
{
    let date = $('[name=date]').val();
    window.location.replace("/logs/search/" + date);
    return false;
}

function show_menu() {
    let x = document.getElementsByClassName("menu-bar")[0];
    if (x.id === "menu-close") {
        x.id = "menu-open";
    } else {
        x.id = "menu-close";
    }
}