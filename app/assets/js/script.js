
$(document).ready(function () {
    $("#pe_project_id").on("change.select2", function () {
        let projectId = $(this).val();
        fetch(`/get_parameter_employee_payment/${projectId}`)
            .then((response) => response.json())
            .then((data) => {

                let employeeSelect = $("#pe_employee_id");
                employeeSelect.empty();
                data.project_employee.forEach((option) => {
                    employeeSelect.append($('<option>', {
                        value: option.id,
                        text: option.name
                    }));
                });               
                employeeSelect.trigger("change.select2");
         
                let receivedEmployerSelect = $("#pe_received_employer_id");
                receivedEmployerSelect.empty();
                data.project_received_employer.forEach((option) => {
                    receivedEmployerSelect.append($('<option>', {
                        value: option.id,
                        text: option.name
                    }));
                });               
                receivedEmployerSelect.trigger("change.select2");
                
            })
            .catch((error) => console.error("Error fetching data:", error));
    });
});


$(document).ready(function () {
    $("#re_project_id").on("change.select2", function () {
        let projectId = $(this).val();
        console.log("Selected Project ID:", projectId);
        fetch(`/get_statutory_deductions/${projectId}`)
            .then((response) => response.json())
            .then((data) => {                
                document.getElementById("insurance_percentage").value = data[0].contract_insurance_percentage;
                document.getElementById("guarantee_performance_percentage").value = data[0].contract_guarantee_performance_percentage;
                document.getElementById("university_overhead_percentage").value = data[0].contract_university_overhead_percentage;
                document.getElementById("weri_overhead_percentage").value = data[0].contract_weri_overhead_percentage;
                document.getElementById("tax_percentage").value = data[0].contract_tax_percentage;            
            })
            .catch((error) => console.error("Error fetching data:", error));
    });
});