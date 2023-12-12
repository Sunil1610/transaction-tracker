// document.getElementById('scrapeButton').addEventListener('click', function() {
//     chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
//       chrome.tabs.sendMessage(tabs[0].id, { action: 'scrapeWebPage' });
//     });
//   });
// chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
//   if (changeInfo.status == "complete") {
//     chrome.tabs.sendMessage(tabId, {method: "getData"});
//   }
// });

console.log("Hi from background Script file")

// chrome.runtime.onMessage.addListener( function (request, sender, sendResponse) {
//     console.log("Got message from content Script: ", request);
//     sendResponse('OK');
// })

// chrome.action.onClicked.addListener((tab) => {
//   chrome.scripting.executeScript({
//     target: { tabId: tab.id },
//     files: ['content.js']
//   });
// });

// document.getElementById('fetchTransactions').addEventListener('click', function() {
//   // Get the current active tab
//   chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
//       var currentTab = tabs[0];
//       // Inject the content script into the current tab
//       chrome.scripting.executeScript({
//           target: { tabId: currentTab.id },
//           files: ['content.js']
//       });
//   });
// });
document.addEventListener('DOMContentLoaded', function () {
  
chrome.cookies.getAll({}, function(cookies) {
  console.log('here');
  console.log(cookies);
  for(let i = 0; i < cookies.length; i++) {
    console.log(cookies[i]);
  }
});
  document.getElementById('fetchTransactions').addEventListener('click', function() {
    var selectedValue = document.getElementById('dropdown').value;
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {action: "fetchTransactions", dropdownValue: selectedValue}, function(response) {
        console.log(response);
      });
    });
  });
});
chrome.cookies.getAll({}, function(cookies) {
  console.log('here');
  console.log(cookies);
  for(let i = 0; i < cookies.length; i++) {
    console.log(cookies[i]);
  }
});
console.log(chrome.cookies);
console.log(chrome);