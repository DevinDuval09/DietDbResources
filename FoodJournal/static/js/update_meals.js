let current_address = window.location.pathname.split("/")
//document.addEventListener("change", display_calories)
let start_date = document.getElementById("start_date");
let end_date = document.getElementById("end_date");
let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value;

function update_data(){
        data_address = "/" + current_address[1] + "/" + current_address[2] + "/" + start_date.value + "/" + end_date.value + "/";
        console.log(data_address);
        location.replace(data_address);
}

start_date.addEventListener("change", update_data);
end_date.addEventListener("change", update_data);