// chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
//     if (request.action === 'scrapeWebPage') {
//       // Perform scraping operations (replace this with your specific scraping code)
//       // For example, let's get the title of the webpage
//       var pageTitle = document.title;

//       console.log('Web page title:', pageTitle);
//     }
//   });
// chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
//   if (request.method == "getData") {
//     var data = document.body.textContent;
//     sendResponse({data: data});
//   }
// }); 
console.log("Hi from content script");

// chrome.runtime.sendMessage({ data: document }, function (response) {
//     console.log(response);
// });
// 
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === 'fetchTransactions') {
    var limit = 1;
    if (request.action === 'fetchTransactions') {
      limit = request.dropdownValue;
      console.log(limit);
    }
    console.log(document.title);
    if (document.title.includes("Amazon Pay")) {
      for (let i = 0; i < limit; i++) {
        setTimeout(function () {
          // Scroll to the bottom of the page
          window.scrollTo(0, document.body.scrollHeight);
        }, 2000 * i);
      }
      setTimeout(function () {
      const transactions = document.querySelectorAll('#itemDetailExpandedView.a-declarative');
      const transactionData = [];
      if (transactions.length > 0) {
        transactions.forEach((transaction) => {
          additionalDetails = [];
          transaction.querySelectorAll('.a-row.pad-mini-details-text').forEach(
            (node)=>{
              additionalDetails.push(node.innerText.trim().replace(/\s+/g, ' '));
          });
          const transactionDetails = {
            "transaction_str" : transaction.innerText.trim(),
            additionalDetails
          }
          transactionData.push( transactionDetails );
        });
        // console.log('Transactions:', transactionData);
      } else {
        console.log('No transactions found on this page.');
      }
      console.log(transactionData)
      fetch('http://localhost:8000/api/upload/amazon_pay', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(transactionData),
      })
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
      }, 2000 * limit);
    } else if (document.title.includes("Splitwise")) {
      // Wait for a while to let the page load
      for (let i = 0; i < limit; i++) {
        setTimeout(function () {
          // Scroll to the bottom of the page
          // window.scrollTo(0, document.body.scrollHeight);
          var button = document.getElementById('load_more_expenses_button');
          button.click();
        }, 2000*i);
      }
      setTimeout(function () {
        console.log("End of all shit");
        const transactions = document.querySelectorAll('.expense.summary.involved');
        console.log(transactions);
        const transactionData = [];
        if (transactions.length > 0) {
          transactions.forEach((transaction) => {
            const date = transaction.getAttribute('data-date');
            const description = transaction.querySelector('.description').innerText;
            const cost = transaction.querySelector('.cost').innerText;
            const you = transaction.querySelector('.you').innerText;
            transactionData.push({
              date, cost, you, description
            });
          });
        } else {
          console.log('No transactions found on this page.');
        }
        fetch('http://localhost:8000/api/upload/splitwise', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(transactionData),
        })
          .then(response => response.json())
          .then(data => {
            console.log('Success:', data);
          })
          .catch((error) => {
            console.error('Error:', error);
          });
      }, 2000 * limit);
    }
  }
  sendResponse({ status: "Script run successfully" });
});