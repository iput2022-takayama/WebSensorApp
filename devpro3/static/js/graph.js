document.addEventListener('DOMContentLoaded', function(){
    const form = document.getElementById('temperature-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
        
            fetch('/add_data', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('G-1：データは正常に追加されました\n湿度・大気圧・CO2濃度データは平均を入力されます\nページの再読み込みを行います');
                    location.reload();  // ページを再読み込みしてデータを更新
                } else {
                    alert('Failed to add data: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Fetch Error:', error);       // データの追加中のエラー
                alert('An error occurred while adding data');
            })
        })
    } else {
        console.error('Form with id "temperature-form" not found.');
    }

    fetch('/data')
        .then(response => response.json())
        .then(data => {
            updateChartData(data);
            updateAverageValues(data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            alert('Error fetching data: ' + error.message);
        });

    function updateChartData(data) {
        const temperatures = data.map(item => parseFloat(item.Temperature));
        const humidities = data.map(item => parseFloat(item.Humidity));
        const pressures = data.map(item => parseFloat(item.Pressure));
        const co2s = data.map(item => parseFloat(item.CO2));
        const labels = data.map((_, index) => `Data ${index + 1}`);

        const ctx = document.getElementById('sensorChart').getContext('2d');
        if (window.sensorChart && typeof window.sensorChart.destroy === 'function') {
            window.sensorChart.destroy();
        }
        window.sensorChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Temperature (℃)',
                    data: temperatures,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                    fill: false
                }, {
                    label: 'Humidity (%)',
                    data: humidities,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1,
                    fill: false
                }, {
                    label: 'Pressure (hPa)',
                    data: pressures,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    fill: false
                }, {
                    label: 'CO2 (ppm)',
                    data: co2s,
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 1,
                    fill: false
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    function updateAverageValues(data) {
        if (data.length === 0) {
            // データがない場合はNaNを表示
            document.getElementById('average-temperature').textContent = 'NaN';
            document.getElementById('average-humidity').textContent = 'NaN';
            document.getElementById('average-pressure').textContent = 'NaN';
            document.getElementById('average-co2').textContent = 'NaN';
            return;
        }

        const temperatureSum = data.reduce((sum, item) => sum + parseFloat(item.Temperature), 0);
        const humiditySum = data.reduce((sum, item) => sum + parseFloat(item.Humidity), 0);
        const pressureSum = data.reduce((sum, item) => sum + parseFloat(item.Pressure), 0);
        const co2Sum = data.reduce((sum, item) => sum + parseFloat(item.CO2), 0);

        const count = data.length;
        const avgTemperature = (temperatureSum / count).toFixed(2);
        const avgHumidity = (humiditySum / count).toFixed(2);
        const avgPressure = (pressureSum / count).toFixed(2);
        const avgCO2 = (co2Sum / count).toFixed(2);

        document.getElementById('average-temperature').textContent = avgTemperature;
        document.getElementById('average-humidity').textContent = avgHumidity;
        document.getElementById('average-pressure').textContent = avgPressure;
        document.getElementById('average-co2').textContent = avgCO2;
    }
});
