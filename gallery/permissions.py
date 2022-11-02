from rest_framework import permissions

class CustomOnly(permissions.BasePermission):
    def has_permission(self,request,view):

        if request.method == 'GET':#GET과 같은 메소드
            return True
        return request.user.is_authenticated

    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:#GET과 같은 메소드
            return True
        return obj.author == request.user

# class PhotoCustomOnly(permissions.BasePermission):
#     def has_object_permission(self,request,view,obj):
#         if request.method in permissions.SAFE_METHODS:#GET과 같은 메소드
#             return True
#         elif request.method == "POST":
#             return request.user.is_authenticated
#         return obj.plant_id.user == request.user