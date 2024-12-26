from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID, uuid4

from sqlalchemy import TIMESTAMP, BigInteger, CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.meta import Base


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    language_id: Mapped[int] = mapped_column(ForeignKey('languages.id'), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    keys: Mapped[List['Keys']] = relationship('Keys', back_populates='user', cascade='all, delete-orphan')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'language_id': self.language_id,
            'registration_date': self.registration_date.isoformat(),
        }

    __table_args__ = (
        CheckConstraint('user_id > 0', name='ck_users_user_id_positive'),
        UniqueConstraint('user_id', name='uq_users_user_id'),
    )


class Keys(Base):
    __tablename__ = 'keys'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), nullable=False)
    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id'), nullable=False)
    encrypted_key: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    expires_at: Mapped[datetime]

    user: Mapped[User] = relationship('User', back_populates='keys')
    country: Mapped['Countries'] = relationship('Countries')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': str(self.id),
            'user_id': self.user_id,
            'country_id': self.country_id,
            'encrypted_key': self.encrypted_key,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
        }

    __table_args__ = (CheckConstraint('created_at < expires_at', name='ck_keys_dates'),)


class Countries(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    iso_code: Mapped[str] = mapped_column(String, nullable=False)

    keys: Mapped[List['Keys']] = relationship('Keys', back_populates='country', cascade='all, delete-orphan')

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'iso_code': self.iso_code,
        }

    __table_args__ = (CheckConstraint('length(iso_code) = 2', name='ck_countries_iso_code_length'),)


class Languages(Base):
    __tablename__ = 'languages'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    locale: Mapped[str] = mapped_column(String, nullable=False)

    users: Mapped[List['User']] = relationship('User', back_populates='language', cascade='all, delete-orphan')

    __table_args__ = (CheckConstraint('length(locale) > 0', name='ck_languages_locale_length'),)
