chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url) {
        // Skip chrome:// URLs and other restricted URLs
        if (tab.url.startsWith('chrome://') || tab.url.startsWith('about:')) {
            console.log("Skipping restricted URL:", tab.url);
            return; // Do nothing for chrome:// and about: URLs
        }

        // Proceed only if the URL is allowed
        chrome.scripting.executeScript({
            target: { tabId: tabId },
            func: captureDomData
        }).then(() => {
            console.log("DOM captured successfully.");
        }).catch(err => {
            console.error("Error capturing DOM:", err);
        });
    }
});

// Function to capture DOM data
function captureDomData() {
    const capturedData = {
        url: window.location.href,
        title: document.title,
        entryTime: Date.now(),
        renderedHtml: document.documentElement.outerHTML
    };

    chrome.runtime.sendMessage({ action: 'sendData', data: capturedData });
}

function sendToAPI(data) {
    console.log("Captured Data:", data);

    fetch('http://localhost:8080/endpoint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)  // Send the captured data as JSON
    })
        .then(response => response.json())
        .then(res => {
            console.log('Data successfully sent to the API:', res);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'sendData') {
        sendToAPI(message.data);
    }
});
