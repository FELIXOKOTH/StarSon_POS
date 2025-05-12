# Simulated role and shift logic
class Role:
    def __init__(self, name, can_edit_backend, can_view_reports, can_access_core):
        self.name = name
        self.can_edit_backend = can_edit_backend
        self.can_view_reports = can_view_reports
        self.can_access_core = can_access_core

class UserShift:
    def __init__(self, user, role, shift_start, shift_end=None):
        self.user = user
        self.role = role
        self.shift_start = shift_start
        self.shift_end = shift_end
