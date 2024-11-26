
// select avtice link in nav
const navItems = document.querySelectorAll('.nav-item');
console.log(navItems)
navItems.forEach(item => {
  item.addEventListener('click', () => {
    navItems.forEach(nav => nav.classList.remove('active'));
    item.classList.add('active');
  });
});

// search box display/ hidden in nav
searchToggle = document.getElementById('search-toggle');
searchBox = document.getElementById('search-box');
if (searchToggle){
  searchToggle.addEventListener('click', ()=>{
    console.log('Hi')
    if(searchBox.classList.contains('hidden')){
      searchBox.classList.remove("hidden");
    }else{
      searchBox.classList.add("hidden");
    }
  })
}

