from webks import admin, db
from flask import redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from webks.models import RoomCatalog, Room, Manager, Employee, Customer




#tạo ra thêm thêm một trang About Us
class AboutUsView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/about-us.html")


#tạo ra Logout khi đăng nhập thành công, nhấn Logout để thoát và trở về lại trang admin
class LogOutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated


#tạo thuộc tính ẩn khi chưa đăng nhập/hiện khi đăng nhập thành công
class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(AuthenticatedView(RoomCatalog, db.session))
admin.add_view(AuthenticatedView(Room, db.session))
admin.add_view(AuthenticatedView(Manager, db.session))
admin.add_view(AuthenticatedView(Employee, db.session))
admin.add_view(AuthenticatedView(Customer, db.session))
admin.add_view(AboutUsView(name="About Us"))
admin.add_view(LogOutView(name="Log Out"))