base_address = "/FoodInfo/get_food_json/"
document.addEventListener("change", display_calories)
calorie_label = document.getElementById("total_cals");
calories_unit_label = document.getElementById("unit_cals");
qty_input = document.getElementsByName("qty_input")[0];
food_input = document.getElementsByName("food_input")[0];
csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value

function display_calories(){
    food = food_input.value.trim();
    console.log(food);
    if (food !== null && food !== "") {
        food_request = new XMLHttpRequest();
        food_data_address = base_address + food + "/";
        food_request.open("GET", food_data_address, false);
        food_request.setRequestHeader("Content-type", "application/x-www-urlencoded");
        food_request.setRequestHeader("X-CSRFToken", csrf_token );
        food_request.onreadystatechange = function() {
            if(food_request.readyState == 4 && food_request.status == 200){
                data = JSON.parse(food_request.responseText);
                qty = Number(qty_input.value);
                total_calories = qty * data["calories_unit"]
                console.log("total calories:")
                console.log(total_calories)
                calorie_label.innerHTML = String(total_calories)
            };
        };
    food_request.send(null);
    };

}