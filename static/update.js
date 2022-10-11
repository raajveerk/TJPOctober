// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

var input_OPENBUY_CHECK = document.getElementById("openBuyfirst");
input_OPENBUY_CHECK.addEventListener("change", function()
{
  if (this.checked){
    openBuyfirst_defaultcheck();
    openOrNotBuy();
    console.log("Hellobc" );
  }
  else {
    console.log("Not checked");
    openOrNotBuy();
    openBuyfirst_CheckBox_Chod();
  }
});


var input_OPENSELL_CHECK = document.getElementById("openSell");
input_OPENSELL_CHECK.addEventListener("change", function()
{
  if (this.checked){
    openSellfirst_defaultcheck();
    openOrNotSell();
    console.log("Hellobc" );
  }
  else {
    console.log("Not checked");
    openOrNotSell();
    openSellfirst_CheckBox_Chod()
  }
});



// When the user clicks the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}


console.log("HELLLLLLLLOOOOOOOOOOOOO", document.getElementById("openBuyfirst").value, document.getElementById("openBuyfirst").checked);
// Reveal Lot Size and No. of Lots when either of Futures, Call or Put is selected
var intialInstrument = document.getElementById("can");
intialInstrument = intialInstrument.style.display = "none";



function openBuyfirst_defaultcheck(){
  document.getElementById("openBuyfirst_defaultcheck").value="OPENBUY_ye"
  console.log("OPEN BUY TRADE", document.getElementById("openBuyfirst_defaultcheck").value)
  console.log("cha raha hun")
}   

function openBuyfirst_CheckBox_Chod(){
  document.getElementById("openBuyfirst_defaultcheck").value="OPENBUY_no"
  console.log("Problem in Buy Open")
  // document.getElementById("openBuy").checked=false

}

function openSellfirst_CheckBox_Chod(){
  document.getElementById('openSELLfirst_defaultcheck').value="OPENSELL_no"
  console.log("Problem in Buy Sell")
  // document.getElementById("openSell").checked=false
}

function openSellfirst_defaultcheck(){
  document.getElementById('openSELLfirst_defaultcheck').value="OPENSELL_ye"
  console.log("OPEN SELL TRADE",document.getElementById('openSELLfirst_defaultcheck').value )
}



function text(x) {
  if (x == 0) {
    document.getElementById("can").style.display = "none";
  }
  else {
    document.getElementById("can").style.display = "block";
  }
  return;
}



// Shuffle Buy/Sell Details depending upon the trade type selected i.e. Buy/Sell
var initialTradeType = document.getElementById("cansell");
initialTradeType = initialTradeType.style.display = "none"; // By default, all the HTML elements are set to 'block'; check modal.css for reference

function tradetype(y) {
  if (y == 0) {
    document.getElementById("canbuy").style.display = "block";
    document.getElementById("cansell").style.display = "none";
  }
  else {
    document.getElementById("canbuy").style.display = "none";
    document.getElementById("cansell").style.display = "block";
  }
  return;
}


if (document.getElementById("buy").checked) {
  tradetype(0)
} else {
  tradetype(1)
}





// CheckBox --> Save as an Open Trade
function openOrNotBuy() {
  var isOpenBuy = document.getElementById("openBuyfirst");
  var showBuy = document.getElementById("canBuyOpen");
  var hidePaisaBuy = document.getElementById("paisa");

  if (isOpenBuy.checked == true) {
    console.log("It's Checked!")
    showBuy = showBuy.style.display = "none";
    hidePaisaBuy = hidePaisaBuy.style.display = "none";
  }
  else {
    showBuy = showBuy.style.display = "block";
    hidePaisaBuy = hidePaisaBuy.style.display = "block";
  }
  return;
}

function openOrNotSell() {
  var isOpenSell = document.getElementById("openSell");
  var showSell = document.getElementById("canSellOpen");
  var hidePaisaSell = document.getElementById("paisa");

  if (isOpenSell.checked == true) {
    console.log("It's Checked as well!")
    showSell = showSell.style.display = "none";
    hidePaisaSell = hidePaisaSell.style.display = "none";
  }
  else {
    showSell = showSell.style.display = "block";
    hidePaisaSell = hidePaisaSell.style.display = "block";
  }
  return;
}


if (document.getElementById("equity").checked == false) {
  text(1)
} else {
  text(0)
}


function ClearFields() {
  document.getElementById("profit").value = "";
  document.getElementById("profitpercent").value = "";
  document.getElementById("sellprice").value = "";
  document.getElementById("sellprice2").value = "";
  document.getElementById("buyprice").value = "";
  document.getElementById("buyprice2").value = "";
  document.getElementById("quantity").value = "";
  document.getElementById("stockname").value = "";
  document.getElementById("nolot").value = "";
  document.getElementById("lotsize").value = "";
}

function quantityCalc(){
  lotsize=document.getElementById("lotsize").value;
  nolot=document.getElementById("nolot").value;
  document.getElementById("quantity").value=lotsize*nolot;
}

// Function to calculate Net Profit & Profit Percentage for the trade type - 'BUY'
function profitcalcBuyandSell() {
  var profit = 0;
  var profit_percent = 0;
  if (document.getElementById("buy").checked) {
    var value = document.getElementById("sellprice").value;
    console.log("This works")
    console.log(value)
    var x = document.getElementById("buyprice").value;
    console.log(x)
    var y = document.getElementById("quantity").value;
    var lotsize=document.getElementById("lotsize").value;
    var nolot=document.getElementById("nolot").value;
    console.log(y)
    console.log("This works 6999")

    if (document.getElementById("equity").checked) {
      profit = (value - x)*y;
      console.log(profit);
      profit_percent = ((value - x)/x)*100;

    } else {
      profit = (value - x)*(lotsize*nolot);
      profit_percent = ((value - x)/x)*100;
    }
    console.log(profit_percent);
    console.log("This works 7999")
    document.getElementById("profit").value = profit;
    console.log("This works 8999")
    document.getElementById("profitpercent").value = profit_percent;
    console.log("This works 9999")

  } else if (document.getElementById("sell").checked) {
    value = document.getElementById("buyprice2").value;
    console.log("This works as well")
    console.log(value)
    var x = document.getElementById("sellprice2").value;
    console.log(x)
    var y = document.getElementById("quantity").value;
    var lotsize=document.getElementById("lotsize").value;
    var nolot=document.getElementById("nolot").value;
    console.log(y)
    console.log("This works 420")
    // var profit = 0;
    // var profit_percent = 0;

    // profit = (x - value)*y;
    // console.log(profit);
    // var profit_percent = 0;
    // profit_percent =((x - value)/value)*100;

    if (document.getElementById("equity").checked) {
      profit = (x - value)*y;
      console.log(profit);
      profit_percent = ((x - value)/value)*100;

    } else {
      profit = (x - value )*(lotsize*nolot);
      profit_percent = ((x - value)/value)*100;
    }
    console.log(profit_percent);
    console.log("This works 7999")
    document.getElementById("profit").value = profit;
    console.log("This works 8999")
    document.getElementById("profitpercent").value = profit_percent;
    console.log("This works 9999")
  }
  
}