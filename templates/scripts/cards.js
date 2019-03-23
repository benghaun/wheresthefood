var header = document.querySelector('header');
var section = document.querySelector('section');

var requestURL = 'http://127.0.0.1:5000/getdeals';
//link of json file here

var request = new XMLHttpRequest();
request.open('GET', requestURL);

request.responseType = 'json';
request.send();

request.onload = function() {
    var discounts = request.response;
    showPlaces(discounts);
  }

function showPlaces(jsonObj) {
    var discounts = jsonObj;
    var row;
    var mainContainer = document.getElementById('maincontainer');
    for (var i = 0; i < discounts.length; i++) {
        if (i % 3 === 0) {
          row = document.createElement('div');
          row.className = 'row justify-content-center';
          mainContainer.appendChild(row);
        }
        var col = document.createElement('div');
        col.className = 'col';
        row.appendChild(col);

        //check if address url is there
        if (discounts[i].address_url != null){
          //address
          var address = document.createElement('a');
          address.setAttribute('href', discounts[i].address_url);
        }
        else{
          var address = document.createElement('p');
        }
        
        address.className = "card-subtitle mb-2 text-muted font-small";

        var myArticle = document.createElement('card');
        myArticle.className = "card card-body";

        var days = document.createElement('p');
        var endDate = document.createElement('p');

        //promo name
        var promoName = document.createElement('h6');

        //time info
        var time = document.createElement('p');


        var cardlink = document.createElement('a')
        cardlink.className = "card-link";

        //link discounts to texts
        address.textContent = discounts[i].address_txt;
        days.textContent = discounts[i].days;
        endDate.textContent = 'End date: ' + discounts[i].enddate;
        promoName.textContent = discounts[i].name;
        time.textContent = discounts[i].timeinfo;
        // cardlink.textContent = discounts[i].timing;

        // cardlink.setAttribute('href', discounts[i].timing);

        myArticle.appendChild(promoName);
        myArticle.appendChild(address);
        myArticle.appendChild(days);
        myArticle.appendChild(time);
        myArticle.appendChild(endDate);
        // myArticle.appendChild(cardlink);
        

        col.appendChild(myArticle);
        
    }
    
}