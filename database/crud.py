# crud.py
from sqlalchemy.orm import Session #type: ignore
import uuid
from .schema import Role, Features, Roles_Access_Features, User_Assigned_Role

# Create a new role
def create_new_role(db: Session, role_name: str):
    dbRole = Role(role=role_name)
    db.add(dbRole)
    db.commit()
    db.refresh(dbRole)
    return dbRole

# finding user roles
def find_user_roles(db: Session, user_id: str):
    results = db.query(
        Role.role_id,
        Role.role_type,
        Role.tier
    ).join(User_Assigned_Role, User_Assigned_Role.role_id == Role.role_id)\
    .filter(User_Assigned_Role.user_id == user_id)\
    .all()
    
    return results

# finding features based on role
def find_features_by_role(db: Session, role_id: str):
    results = db.query(
        Features.feature_id,
        Features.feature_name
    ).join(Roles_Access_Features, Roles_Access_Features.feature_id == Features.feature_id)\
    .filter(Roles_Access_Features.role_id == role_id)\
    .all()
    
    return results

# getting all features
def get_all_features(db: Session):
    results = db.query(
        Features.feature_id,
        Features.feature_name
    ).all()
    
    return results
