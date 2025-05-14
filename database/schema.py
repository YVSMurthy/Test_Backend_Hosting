import uuid
from sqlalchemy import create_engine, Column, String, ForeignKey #type: ignore
from sqlalchemy.ext.declarative import declarative_base #type: ignore
from sqlalchemy.orm import relationship, sessionmaker #type: ignore
from sqlalchemy.dialects.postgresql import UUID #type: ignore

Base = declarative_base()

# define the database models
class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(String, unique=True, nullable=False)

class Features(Base):
    __tablename__ = 'features'
    feature_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    feature = Column(String, unique=True, nullable=False)

class Roles_Access_Features(Base):
    __tablename__ = 'roles_access_features'
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.role_id', ondelete='CASCADE'), primary_key=True)
    feature_id = Column(UUID(as_uuid=True), ForeignKey('features.feature_id', ondelete='CASCADE'), primary_key=True)
    role = relationship("Role")
    feature = relationship("Features")

class User_Assigned_Role(Base):
    __tablename__ = 'user_assigned_role'
    user_id = Column(UUID(as_uuid=True), ForeignKey('auth.users.id', ondelete='CASCADE'), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.role_id', ondelete='CASCADE'), primary_key=True)
    role = relationship("Role")

