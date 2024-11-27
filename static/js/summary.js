// Graph functions for service vs Service Requests 
if(serviceRequestlabels && serviceRequestdatasets ){
    const serviceRequestdata = {
        labels: serviceRequestlabels,
        datasets: serviceRequestdatasets
    };
    
    const serviceRequestConfig = {
        type: 'bar',
        data: serviceRequestdata,
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Services vs Service Requests'
                },
            },
            responsive: true,
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true,
                }
            }
        }
    };
    
    new Chart(document.getElementById('services_vs_serviceRequests'), serviceRequestConfig);
}




// Graph functions for service vs Professioanls 
if(professionallabels && professionaldatasets){
    const professioanlsdata = {
        labels: professionallabels,
        datasets: professionaldatasets
    };
    
    
    const professionalConfig = {
        type: 'bar',
        data: professioanlsdata,
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Services vs Professionals'
                },
            },
            responsive: true,
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true,
                }
            }
        }
    };
    
    new Chart(document.getElementById('services_vs_professionals'), professionalConfig);
}


// Pie chart for service request Status

if (statusdata && statusLabels){
    statusDataset = [
        {
            label: 'No. of service Requests',
            data: statusdata, // Count of requests per status
            backgroundColor: [
                '#FFA500', // Pending
                '#5DA5DA', // Accepted
                '#60BD68', // Completed
                '#B276B2', // Closed
                '#E16851', // Rejected
            ],
            hoverOffset: 4
        }
    ] 
    
    
    const statusConfig = {
        type: 'pie',
        data:{
            labels: statusLabels,
            datasets: statusDataset
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Service Request Status Distribution'
                },
            },
            responsive: true
        }
    }
    
    new Chart(document.getElementById('statusPieChart'), statusConfig )
    
}



