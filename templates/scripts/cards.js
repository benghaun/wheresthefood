var header = document.querySelector('header');
var section = document.querySelector('section');

var requestURL = '/getdeals';
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
    var row = document.getElementById('cardRow');
    var mainContainer = document.getElementById('maincontainer');
    
    for (var i = 0; i < discounts.length; i++) {
        
        var col = document.createElement('div');
        col.className = 'column card';
        // row.appendChild(col);

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

        var myArticle = document.createElement('a');
        myArticle.className = "card-body column-img";
        myArticle.setAttribute('href', "/?selected="+discounts[i].name);

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
        endDate.textContent = 'Ends ' + discounts[i].enddate.substring(0, discounts[i].enddate.length-13);
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
        row.appendChild(col);
    }
    
}