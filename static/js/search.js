searchToggle = document.getElementById('search-toggle');
searchBox = document.getElementById('search-box');
if (searchToggle){
    if(searchBox.classList.contains('hidden')){
      searchBox.classList.remove("hidden");
    }
}