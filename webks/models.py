from sqlalchemy import Column, Integer, Float, String,  Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from enum import Enum as UserEnum
from webks import db
from datetime import datetime


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class SaleBase(db.Model):
    __abstract__ = True

    def __str__(self):
        return self.name


#Tạo csdl để lưu trữ thông tin đăng nhập của một user
class User(SaleBase, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100))
    username = Column(String(50), nullable=True, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100))
    active = Column(Boolean, default=True)
    #user_role = Column(Enum(UserRole), default=UserRole.USER)
    customer = relationship('Customer', back_populates="user")


#Tạo csdl của danh mục phòng
class RoomCatalog(SaleBase):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    note = Column(String(255))
    rooms = relationship('Room', backref='roomcatalog', lazy=True)


#Tạo csdl của phòng
class Room(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_number = Column(String(20), nullable=False)
    description = Column(String(255))
    price = Column(Float, default=0)
    image = Column(String(100))
    RoomCatalog_id = Column(Integer, ForeignKey(RoomCatalog.id), nullable=False)

    customers = relationship('Customer', backref='room', lazy=True)


#Tạo csdl về thông tin cá nhân của Customer, manager, employee
class PersonalInfo(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(50), nullable=False)
    lastname = Column(String(10), nullable=False)
    firstname = Column(String(10), nullable=False)
    id_card = Column(String(15), nullable=False)
    address = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    email = Column(String(20), nullable=True)

    def __str__(self):
        return self.name


#Tạo csdl của người quản lý khách sạn
class Manager(PersonalInfo):

    employees = relationship('Employee', backref='manager', lazy=True)


#Tạo csdl của nhân viên khách sạn
class Employee(PersonalInfo):

    office = Column(String(20), nullable=False)
    manager_id = Column(Integer, ForeignKey(Manager.id), nullable=False)
    customers = relationship('Customer', backref='employee', lazy=True)


#tạo csdl của khách hàng
class Customer(PersonalInfo):

    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    employee_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship('User', back_populates="customer", uselist=False)


#tạo csdl của bảng hóa đơn
class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.today())
    customer_id = Column(Integer, ForeignKey(User.id))
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)


#tạo csdk=l của bảng chi thiết hóa đơn
class ReceiptDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    quantity = Column(Integer, default=0)
    price = Column(Integer, default=0)


if __name__ == "__main__":
    db.create_all()