// Voice recognition setup
let recognition;
let isListening = false;

// Initialize speech recognition if available
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = function() {
        isListening = true;
        updateVoiceStatus('Listening... Speak now!', 'listening');
        document.getElementById('voiceBtn').classList.add('listening');
    };

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById('searchInput').value = transcript;
        updateVoiceStatus('Processing voice command...', 'processing');
        
        // Process voice command
        setTimeout(() => {
            processVoiceCommand(transcript);
        }, 500);
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        updateVoiceStatus('Voice recognition error. Please try again.', 'error');
        resetVoiceButton();
    };

    recognition.onend = function() {
        resetVoiceButton();
    };
}

// Voice button click handler
document.getElementById('voiceBtn').addEventListener('click', function() {
    if (!recognition) {
        showStatus('Voice recognition is not supported in your browser.', 'error');
        return;
    }

    if (isListening) {
        recognition.stop();
        resetVoiceButton();
    } else {
        recognition.start();
    }
});

// Process voice commands intelligently
function processVoiceCommand(transcript) {
    const command = transcript.toLowerCase();
    
    // Extract search type and query from voice command
    if (command.includes('youtube') || command.includes('video')) {
        const query = extractQuery(command, ['youtube', 'video', 'search', 'for', 'on']);
        if (query) {
            document.getElementById('searchInput').value = query;
            performSearch('youtube');
        }
    } else if (command.includes('google') || command.includes('search')) {
        const query = extractQuery(command, ['google', 'search', 'for', 'on']);
        if (query) {
            document.getElementById('searchInput').value = query;
            performSearch('google');
        }
    } else if (command.includes('instagram') || command.includes('insta')) {
        const query = extractQuery(command, ['instagram', 'insta', 'profile', 'user', 'find', 'on']);
        if (query) {
            document.getElementById('searchInput').value = query;
            performSearch('instagram');
        }
    } else {
        // Default to Google search if no specific platform mentioned
        updateVoiceStatus('No specific platform detected. Ready for manual search.', '');
    }
}

// Extract meaningful query from voice command
function extractQuery(command, stopWords) {
    let words = command.split(' ');
    let queryWords = [];
    let foundStopWord = false;
    
    for (let word of words) {
        if (stopWords.includes(word)) {
            foundStopWord = true;
            continue;
        }
        if (foundStopWord || !stopWords.some(sw => command.indexOf(sw) < command.indexOf(word))) {
            queryWords.push(word);
        }
    }
    
    return queryWords.join(' ').trim();
}

// Update voice status display
function updateVoiceStatus(message, type) {
    const statusElement = document.getElementById('voiceStatus');
    statusElement.querySelector('.status-text').textContent = message;
    statusElement.className = `voice-status ${type}`;
}

// Reset voice button state
function resetVoiceButton() {
    isListening = false;
    document.getElementById('voiceBtn').classList.remove('listening');
    setTimeout(() => {
        updateVoiceStatus('Click the microphone to start voice recognition', '');
    }, 2000);
}

// Perform search function
async function performSearch(platform) {
    const query = document.getElementById('searchInput').value.trim();
    
    if (!query) {
        showStatus('Please enter a search query or use voice input.', 'error');
        return;
    }

    try {
        showStatus('Processing your request...', 'success');
        
        const response = await fetch(`/api/search/${platform}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();

        if (data.success) {
            showStatus(data.message, 'success');
        } else {
            showStatus(data.error || 'An error occurred', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showStatus('Network error. Please try again.', 'error');
    }
}

// Show status message
function showStatus(message, type) {
    const statusElement = document.getElementById('statusMessage');
    statusElement.textContent = message;
    statusElement.className = `status-message ${type} show`;
    
    setTimeout(() => {
        statusElement.classList.remove('show');
    }, 4000);
}

// Enter key handler for search input
document.getElementById('searchInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        // Default to Google search when pressing Enter
        performSearch('google');
    }
});

