__author__ = 'Omkareshwar'


class Vendor:
    address = ''
    phone = ''
    name = ''
    footfall = ''
    email = ''
    status = False

    def __init__(self, data, db):
        self.address = data['address']
        self.phone = data['phone']
        self.name = data['business']
        self.email = data['email']
        self.footfall = data['footfall']
        db.insert(
            {'address': data['address'], 'phone': data['phone'], 'name': data['business'], 'footfall': data['footfall'],
             'email': data['email'], 'status': False})


    def update_status(self, val, eid, db):
        """

        :type val: bool
        """
        assert isinstance(val, bool)
        self.status = val
        db.update({'status': val}, eids[eid])
