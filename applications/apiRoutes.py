from applications.apiControllers import *

def initializeUserRoutes(api):
    api.add_resource(RegisterController, '/api/userregister')
    api.add_resource(deleteUserController, '/api/deleteUser')