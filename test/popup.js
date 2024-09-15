
document.getElementById('captureDom').addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            func: captureDomData
        });
    });
});

function captureDomData() {
    const capturedData = {
        url: window.location.href,
        title: document.title,
        entryTime: Date.now(),
        renderedHtml: document.documentElement.outerHTML
    };

    chrome.runtime.sendMessage({ action: 'sendData', data: capturedData });
}
