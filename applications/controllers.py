from applications.models import *
from collections import defaultdict


def getServiceRequestStackBarChartData(user):
    # Query services and their service history
    services = Services.get_active_services().all()
    service_data = defaultdict(lambda: [0, 0, 0, 0, 0])  # For statuses 0-5

    for service in services:
        if user.role == 'admin':
            histories = ServiceHistory.get_active_serviceHistory().filter_by(servicesId=service.id).all()
        elif user.role == 'client':
            histories = ServiceHistory.get_active_serviceHistory().filter(ServiceHistory.servicesId == service.id, ServiceHistory.customerId == user.customerDetails.id).all()
         
        for history in histories:
            service_data[service.name][history.status] += 1


    # Convert to labels and datasets for Chart.js
    labels = list(service_data.keys())
    datasets = [
        {"label": "Pending", "data": [data[0] for data in service_data.values()], "backgroundColor": "#FFA500"},
        {"label": "Accepted", "data": [data[1] for data in service_data.values()], "backgroundColor": "#5DA5DA"},
        {"label": "Completed", "data": [data[2] for data in service_data.values()], "backgroundColor": "#60BD68"},
        {"label": "Closed", "data": [data[3] for data in service_data.values()], "backgroundColor": "#B276B2"},
        {"label": "Rejected", "data": [data[4] for data in service_data.values()], "backgroundColor": "#E16851"},
    ]

    return labels, datasets

def getProfessionalStackBarChartData():
    # Query services and their service history
    services = Services.get_active_services().all()
    professional_data = defaultdict(lambda: [0, 0, 0])  # For professional statuses 0-5


    for service in services:
        professionals = Professionals.get_all_professionals().filter_by(serviceId=service.id).all()
        for professional in professionals:
            if professional.is_rejected:
                professional_data[service.name][1] += 1
            elif professional.is_blocked:
                professional_data[service.name][2] += 1
            else:
                professional_data[service.name][0] += 1


    professionalLabels = list(professional_data.keys())
    # Convert to labels and datasets for Chart.js
    professionalDatasets = [
        {"label": "Active", "data": [data[0] for data in professional_data.values()], "backgroundColor": "#60BD68"}, 
        {"label": "Rejected", "data": [data[1] for data in professional_data.values()], "backgroundColor": "#E16851"}, 
        {"label": "Blocked", "data": [data[2] for data in professional_data.values()], "backgroundColor": "#B276B2"}, 
    ]

    return professionalLabels, professionalDatasets

def getServiceRequestStatus(user):
    if user.role == 'admin':
        status_counts = db.session.query(ServiceHistory.status, db.func.count(ServiceHistory.id)).filter(ServiceHistory.is_deleted == False).group_by(ServiceHistory.status).all()
    elif user.role == 'client':
        status_counts = db.session.query(ServiceHistory.status, db.func.count(ServiceHistory.id)).filter(ServiceHistory.is_deleted == False, ServiceHistory.customerId == user.customerDetails.id).group_by(ServiceHistory.status).all()
    else:
        status_counts = db.session.query(ServiceHistory.status, db.func.count(ServiceHistory.id)).filter(ServiceHistory.is_deleted == False, ServiceHistory.professionalId == user.professionalDetails.id).group_by(ServiceHistory.status).all()
    status_labels = {
        0: 'Pending',
        1: 'Accepted',
        2: 'Completed',
        3: 'Closed',
        4: 'Rejected'
    }

    statusLabels = [status_labels[status[0]] for status in status_counts]
    statusdata  = [status[1] for status in status_counts]
    
    return statusLabels, statusdata