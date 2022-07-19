base_address = "/FoodInfo/get_food_json/"
//document.addEventListener("change", display_calories)
calorie_label = document.getElementById("total_cals");
calories_unit_label = document.getElementById("unit_cals");
qty_input = document.getElementsByName("qty_input")[0];
food_input = document.getElementsByName("food_input")[0];
food_id = document.getElementsByName("food_id")[0];
csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value
errors = document.getElementById("errors")
data = null

function display_calories(){
    //if qty is not null, and data is not null
    if (qty_input.value !== "" && qty_input.value !== null && data !== null && !data.hasOwnProperty("error")){
        qty = Number(qty_input.value);
        total_calories = qty * data["calories_unit"];
        food_id.value = data["id"];
        console.log("total calories:");
        console.log(total_calories);
        calorie_label.innerHTML = String(total_calories);
        errors.setAttribute("hidden", "hidden");
    }
};

function get_food_data(){
    //clean food input
    food = food_input.value.trim();
    console.log("Getting " + food);
    //create request to get json
    if (food !== null && food !== "") {
        food_request = new XMLHttpRequest();
        food_data_address = base_address + food + "/";
        food_request.open("GET", food_data_address, false);
        food_request.setRequestHeader("Content-type", "application/x-www-urlencoded");
        food_request.setRequestHeader("X-CSRFToken", csrf_token );
        food_request.onreadystatechange = function() {
            if(food_request.readyState == 4 && food_request.status == 200){
                data = JSON.parse(food_request.responseText);
                console.log(data)
                if (!data.hasOwnProperty("error")){
                    errors.setAttribute("hidden", "hidden");
                    //try to display calories
                    display_calories();
                } else {
                    errors.removeAttribute("hidden");
                    errors.innerHTML = data["error"];
                    calorie_label.innerHTML = "";
                }
            };
        };
    food_request.send(null);
    };

}
qty_input.addEventListener("change", display_calories)
food_input.addEventListener("change", get_food_data);
