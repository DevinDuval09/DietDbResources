let summaries = new Array();
let cals_summary = {"element": document.getElementById("avg_calories"),
                    "values": document.getElementsByName("calories")};
summaries.push(cals_summary)
let prot_summary = {"element": document.getElementById("avg_protein"),
                    "values": document.getElementsByName("protein")};
summaries.push(prot_summary)
let carbs_summary = {"element": document.getElementById("avg_carbs"),
                    "values": document.getElementsByName("carbs")};
summaries.push(carbs_summary)
let fat_summary = {"element": document.getElementById("avg_fat"),
                    "values": document.getElementsByName("fat")};
summaries.push(fat_summary)
let sat_fat_summary = {"element": document.getElementById("avg_sat_fat"),
                        "values": document.getElementsByName("sat_fat")};
summaries.push(sat_fat_summary)
let fiber_summary = {"element":document.getElementById("avg_fiber"),
                    "values": document.getElementsByName("fiber")};

function post_summaries(sum_array) {
    for (let i = 0; i < sum_array.length; ++i){
        summary = sum_array[i]
        sum = 0;
        values = summary["values"]
        for (const element of values){
            console.log(element.innerHTML)
            sum += Number(element.innerHTML)
        };
        summary["element"].innerHTML = sum / values.length;
    }
}

window.onload = post_summaries(summaries);