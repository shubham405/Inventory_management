Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';
var ctx = document.getElementById("predictionPieChart");
var valueLabel = document.getElementById("valueLabel");

var data = {
  
  datasets: [{
    data: [55, 30],
    backgroundColor: ['#FFCCFF', '#17a673'],
    hoverBackgroundColor: ['#FFCCFF', '#17a673'],
    hoverBorderColor: "rgba(234, 236, 244, 1)",
  }],
};

var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: data,
  options: {
    maintainAspectRatio: false,
    cutoutPercentage: 80,
    tooltips: {
      enabled: false
    }
  }
});

// Function to update the chart data and display the value inside the circle
function updateChartData(fraud, notFraud) {
  data.datasets[0].data = [fraud, notFraud];
  if(fraud<=30)
  {
    color1 = '#55FF33'
  }
  else if(fraud>30 && fraud<=50)
  {
    color1 = '#FFFF00'
  }
  else if(fraud>50 && fraud<80)
  {
    color1 = '#ff6347'
  }
  else
  {
    color1 = '#ff0800'
  }
  color2 = '#FFCCFF'
  data.datasets[0].backgroundColor=[color1,color2]
  data.datasets[0].hoverBackgroundColor=[color1,color2]
  myPieChart.update();
  
  // Display the value inside the circle
  valueLabel.textContent = (fraud  + "%")   ;
}

// Example usage: Update the chart with new data (e.g., fraud = 60, notFraud = 40)
let fraudScore = document.getElementById('fraudScore').textContent*100;
updateChartData(fraudScore, 100-fraudScore);
function clearPlaceholder() {
    var timeInput = document.getElementById('txnTime');
    timeInput.placeholder = '';
}

// Function to restore the placeholder when the input is blurred and empty
function restorePlaceholder() {
    var timeInput = document.getElementById('txnTime');
    
    if (!timeInput.value.trim()) {
        timeInput.placeholder = 'Transaction Time';
    }
}
function validateInput(input) {
    input.value = input.value.replace(/\D/g, ''); // Remove non-numeric characters
}
        var currentDate = new Date();
        var currentDay = currentDate.getDate().toString().padStart(2, '0');
        var currentYear = currentDate.getFullYear();
        var currentMonth = (currentDate.getMonth() + 1).toString().padStart(2, '0'); // Adding 1 because months are zero-indexed

        // Set the maximum allowed value dynamically
        document.getElementById('expDate').setAttribute('min', currentYear + '-' + currentMonth);
        document.getElementById('expDate').setAttribute('value', currentYear + '-' + currentMonth);
        document.getElementById('accountOpenDate').setAttribute('max', currentYear + '-' + currentMonth + '-' + currentDay);

        function showModal(fraudScore) {
            // Update the modal body content with the custom message
            let message = `Every thing is ok !, Your fraud score is ${fraudScore} %`;
            if(fraudScore>= 30 && fraudScore <40)
            {
                message= `MFA 1 required !, Your fraud score is ${fraudScore} %`;
            }
            else if (fraudScore>=40 && fraudScore<50)
            {
                message = `MFA 2 required !, Your fraud score is ${fraudScore} %`;
            }
            else if (fraudScore>=50 && fraudScore <60)
            {
                message  = `MFA 3 required !, Your fraud score is ${fraudScore} %`;
            }
            else if(fraudScore>=60)
            {
                message = `Decliend, It is suspesious 1, Your fraud score is {fraudScore} % `;
            }
            document.querySelector('.modal-body').innerHTML = message;
            $('#transactionModal').modal('show');
        }
        
        // Example: Trigger the modal with a custom message
        //var someResult = "This is the result to show in the modal.";
        
        // Check the condition and show the modal if true
        if (fraudScore) {
            showModal(fraudScore);
        }