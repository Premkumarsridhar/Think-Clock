document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();

    var formData = new FormData();
    formData.append('cellImage', document.getElementById('cellImage').files[0]);
    formData.append('cellCondition', document.getElementById('cellCondition').value);
    
    // Additional meta information
    formData.append('nominalVoltage', document.getElementById('nominalVoltage').value);
    formData.append('nominalEnergy', document.getElementById('nominalEnergy').value);
    formData.append('voltageRange', document.getElementById('voltageRange').value);

    fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
          // Display Cell ID and Barcode
          console.log(data);
          document.getElementById('cellIdAndBarcode').innerHTML = 
              'Cell ID: ' + data.cellId + '<br>Barcode: <img src="' + data.barcode + '"/>';
      })
      .catch(error => console.error('Error:', error));
});


document.getElementById('uploadCSV').addEventListener('submit', function(e) {
    e.preventDefault();

    var formData = new FormData();

    formData.append('dataFile', document.getElementById('dataFile').files[0]);


    fetch('http://127.0.0.1:5000/csv', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
          // Use Plotly to plot the data
          var plotData = JSON.parse(data.graphJSON);
          Plotly.newPlot('bodePlotDiv', plotData.data, plotData.layout);
      })
      .catch(error => console.error('Error:', error));
});

// Example function to update the SoH display
function updateSoHDisplay(currentRb, maxRb) {
    var soh = (currentRb / maxRb) * 100;
    document.getElementById('sohValue').innerText = soh.toFixed(2) + '%';
    document.getElementById('sohProgressBar').style.width = soh.toFixed(2) + '%';
}

// Assuming you have the current and maximum values for Rb
var currentRb = 0.015; // Example current value, use actual value from your data
var maxRb = 0.02; // Example max value, replace with the actual max value

updateSoHDisplay(currentRb, maxRb);
