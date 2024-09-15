
(function() {
    const capturedData = {
        url: window.location.href,
        title: document.title,
        entryTime: Date.now(),
        renderedHtml: document.documentElement.outerHTML
    };

    chrome.runtime.sendMessage({ action: 'sendData', data: capturedData });
})();
