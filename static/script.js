function getStockPrice() {
    var symbol = $("#stock-symbol").val();
    if (symbol === "") {
        alert("Please enter a stock symbol.");
        return;
    }

    $.post("/get_price", { symbol: symbol }, function(data) {
        $("#stock-result").html(`Stock: <span class="text-blue-600">${data.symbol}</span> | Price: <span class="text-green-600">$${data.price}</span>`);
    }).fail(function() {
        $("#stock-result").html('<span class="text-red-600">Error fetching stock price.</span>');
    });
}
function toggleTheme() {
  const html = document.documentElement;
  html.classList.toggle('dark');
  localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
}
