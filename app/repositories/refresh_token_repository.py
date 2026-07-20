from uuid import UUID

from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_jti(self, token_jti: str):
        return self.db.query(RefreshToken).filter(RefreshToken.token_jti == token_jti).first()

    def create_refresh_token(self, refresh_token: RefreshToken):
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token

    def revoke_by_jti(self, token_jti: str):
        refresh_token = self.get_by_jti(token_jti)

        if refresh_token:
            refresh_token.revoked = True
            self.db.commit()
            self.db.refresh(refresh_token)

        return refresh_token

    def revoke_all_for_user(self, user_id: UUID):
        self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked.is_(False),
        ).update({"revoked": True})
        self.db.commit()
