document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const analyzeBtn = document.getElementById('analyze-btn');
    const transcriptInput = document.getElementById('transcript');
    const resultsContainer = document.getElementById('results-container');
    const loadingIndicator = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const overallSentiment = document.getElementById('overall-sentiment');
    const overallIntent = document.getElementById('overall-intent');
    const utterancesDiv = document.getElementById('utterances');
    
    // Add event listener to the analyze button
    analyzeBtn.addEventListener('click', analyzeTranscript);
    
    // Function to analyze the transcript
    function analyzeTranscript() {
        // Get the transcript text
        const transcript = transcriptInput.value.trim();
        
        // Validate input
        if (!transcript) {
            alert('Please enter a medical transcript to analyze.');
            return;
        }
        
        // Show loading indicator
        loadingIndicator.classList.remove('hidden');
        resultsDiv.classList.add('hidden');
        
        // Send transcript to the server for analysis
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ transcript: transcript })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Hide loading indicator and show results
            loadingIndicator.classList.add('hidden');
            resultsDiv.classList.remove('hidden');
            
            // Display the results
            displayResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            loadingIndicator.classList.add('hidden');
            alert('An error occurred while analyzing the transcript. Please try again.');
        });
    }
    
    // Function to display analysis results
    function displayResults(data) {
        // Display overall sentiment and intent
        overallSentiment.textContent = data.Overall_Analysis.Sentiment;
        overallSentiment.className = data.Overall_Analysis.Sentiment; // Apply sentiment class
        
        overallIntent.textContent = data.Overall_Analysis.Intent;
        
        // Clear previous utterance analyses
        utterancesDiv.innerHTML = '';
        
        // If no utterances were found
        if (data.Utterance_Analyses.length === 0) {
            utterancesDiv.innerHTML = '<p class="no-utterances">No patient utterances were found in the transcript. Make sure patient lines start with "Patient:".</p>';
            return;
        }
        
        // Display utterance analyses
        data.Utterance_Analyses.forEach((item, index) => {
            const utteranceDiv = document.createElement('div');
            utteranceDiv.className = 'utterance-item';
            
            // Create utterance number and text
            const utteranceNumber = document.createElement('h4');
            utteranceNumber.textContent = `Patient Utterance ${index + 1}`;
            
            const utteranceText = document.createElement('p');
            utteranceText.className = 'utterance-text';
            utteranceText.textContent = `"${item.Utterance}"`;
            
            // Create analysis container
            const analysisDiv = document.createElement('div');
            analysisDiv.className = 'utterance-analysis';
            
            // Create sentiment analysis
            const sentimentDiv = document.createElement('div');
            sentimentDiv.className = `analysis-item ${item.Analysis.Sentiment}`;
            
            const sentimentTitle = document.createElement('h5');
            sentimentTitle.textContent = 'Sentiment';
            
            const sentimentValue = document.createElement('p');
            sentimentValue.textContent = item.Analysis.Sentiment;
            
            sentimentDiv.appendChild(sentimentTitle);
            sentimentDiv.appendChild(sentimentValue);
            
            // Create intent analysis
            const intentDiv = document.createElement('div');
            intentDiv.className = 'analysis-item intent-label';
            
            const intentTitle = document.createElement('h5');
            intentTitle.textContent = 'Intent';
            
            const intentValue = document.createElement('p');
            intentValue.textContent = item.Analysis.Intent;
            
            intentDiv.appendChild(intentTitle);
            intentDiv.appendChild(intentValue);
            
            // Add elements to their containers
            analysisDiv.appendChild(sentimentDiv);
            analysisDiv.appendChild(intentDiv);
            
            utteranceDiv.appendChild(utteranceNumber);
            utteranceDiv.appendChild(utteranceText);
            utteranceDiv.appendChild(analysisDiv);
            
            // Add to the utterances container
            utterancesDiv.appendChild(utteranceDiv);
        });
    }
});