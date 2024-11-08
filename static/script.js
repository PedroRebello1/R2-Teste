function showSection(sectionId) {
    // Esconder todas as seções
    const sections = document.querySelectorAll('.container');
    sections.forEach(section => section.classList.remove('active'));
    
    // Mostrar a seção selecionada
    document.getElementById(sectionId).classList.add('active');
}


document.getElementById('formTrajeto').onsubmit = function(event) {
    event.preventDefault();

    // Show loading animation
    document.getElementById('loadingAnimation').classList.add('active');

    const formData = new FormData(event.target);

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading animation
        document.getElementById('loadingAnimation').classList.remove('active');

        // Update the average risk and plot
        if (data.average_risk) {
            document.getElementById('averageRisk').textContent = `Risco Médio: ${data.average_risk}/10`;
        } else {
            console.warn("data.average_risk not found")
        }
        if (data.plot_url1) {
            document.getElementById('top50').src = 'data:image/png;base64,' + data.plot_url1;
        } else {
            console.warn("plot_url1 is missing from the response.");
        }

        if (data.plot_url2) {
            document.getElementById('dist').src = 'data:image/png;base64,' + data.plot_url2;
        } else {
            console.warn("plot_url2 is missing from the response.");
        }

        if (data.average_frequencia) {
            document.getElementById('averageFrequency').textContent = `Acidentes por ano nas BRs do trajeto: ${data.average_frequencia}`;
        } else {
            console.warn("average_frequencia is missing from the response.");
        }
        
    })
    .catch(error => {
        console.error("Plot URLs not found in the response:", data);
        console.error('Error:', error);
        document.getElementById('loadingAnimation').classList.remove('active');
    });
};
