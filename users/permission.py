from rest_framework import permissions

class CustomReadOnly(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:#GET과 같은 메소드
            return True
        return obj.user==request.user


        # ../permissions.py
