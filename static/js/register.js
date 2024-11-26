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

// Enter value in basic pay

const serviceType = document.getElementById("serviceType");
const basicPayElement = document.getElementById("basicpay");
const smallElement = document.getElementById("totalpay");
const incentiveElement = document.getElementById("incentive");
if(serviceType){
    serviceType.addEventListener("change", ()=>{
        const serviceSelect = serviceType.options[serviceType.selectedIndex];
        const basicPay = serviceSelect.getAttribute("data-baseprice");
        let incentive = incentiveElement.value
        if(!incentive) incentive = 0
        basicPayElement.value = basicPay;
        let totalpay = parseInt(basicPay) + parseInt(incentive);
        smallElement.textContent = `Total amount you will receive  is ₹${basicPay} + ₹${incentive} = ₹${totalpay}`
    })
    
    incentiveElement.addEventListener("change", ()=>{
        let incentive = incentiveElement.value;
        let basicPay = basicPayElement.value;
        if(!basicPay) basicPay = 0
        let totalpay = parseInt(basicPay) + parseInt(incentive);
        smallElement.textContent = `Total amount you will receive  is ₹${basicPay} + ₹${incentive} = ₹${totalpay}`
    })
}

