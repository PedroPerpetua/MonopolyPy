class WrongPasswordException(Exception):
    ''' Raised if the user connects to the server but is disconnected with the wrong password '''

class ServerFullException(Exception):
    ''' Raised if the user connects to the server but is disconnected due to the server being full '''

class ServerOfflineException(Exception):
    ''' Raised if the user fails to reach the server '''


class BadServerException(Exception):
    ''' Raised if the user isn't able to alocate a server @ the specified address'''
