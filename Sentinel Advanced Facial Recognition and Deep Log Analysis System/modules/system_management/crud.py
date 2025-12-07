from modules.system_management.models import UserCreate, User
from config.database import db
from modules.system_management.auth import get_password_hash
import uuid

class UserCRUD:
    def get_user(self, username: str):
        query = "MATCH (u:User {username: $username}) RETURN u"
        with db.neo4j_driver.session() as session:
            result = session.run(query, username=username)
            record = result.single()
            if record:
                node = record["u"]
                return dict(node)
        return None

    def create_user(self, user: UserCreate):
        hashed_pw = get_password_hash(user.password)
        user_id = str(uuid.uuid4())
        query = """
        CREATE (u:User {
            id: $id,
            username: $username,
            email: $email,
            role: $role,
            hashed_password: $hashed_password,
            is_active: true,
            created_at: $created_at
        })
        RETURN u
        """
        params = {
            "id": user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "hashed_password": hashed_pw,
            "created_at": str(datetime.now())
        }
        
        with db.neo4j_driver.session() as session:
            try:
                session.run(query, **params)
                return {**params, "password": user.password} # Return with PW only for confirmation (removed in real response)
            except Exception as e:
                print(f"Error creating user: {e}")
                return None

from datetime import datetime
user_crud = UserCRUD()
