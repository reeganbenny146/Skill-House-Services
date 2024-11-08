// priview profile phot after update 
function previewAvatar() {
    const file = document.getElementById('profileImage').files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('avatarPreview').src = e.target.result;
        }
        reader.readAsDataURL(file); // Read the file as a data URL
    }
}

// select avtice link in nav
const navItems = document.querySelectorAll('.nav-item');
console.log(navItems)
navItems.forEach(item => {
    console.log("Hi")
  item.addEventListener('click', () => {
    navItems.forEach(nav => nav.classList.remove('active'));
    item.classList.add('active');
  });
});