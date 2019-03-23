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
    populateHeader(discounts);
    // showHeroes(discounts);
  }

function showPlaces(jsonObj) {
    var myArticle = document.createElement('article');
    var address = document.createElement('storeAdd');
    var days = document.createElement('storeDays')
    var endDate = document.createElement('storeEnd')
    var promoName = document.createElement('name')
    var storeTime = document.createElement('timing')

    address.textContent = discounts.addresses;
    days.textContent = discounts.days;
    endDate.textContent = 'End date' + discounts.enddate;
    promoName.textContent = 'Name of promo ' + discounts.name;
    storeTime.textContent = discounts.timing;

    myArticle.appendChild(address);
    myArticle.appendChild(days);
    myArticle.appendChild(endDate);
    myArticle.appendChild(promoName);
    myArticle.appendChild(storeTime);
  
    section.appendChild(myArticle);
}