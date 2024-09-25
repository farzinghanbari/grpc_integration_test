from datetime import datetime, timezone

from sqlalchemy.orm import mapped_column, Mapped

from src.sqlalchemy_base import Base


class ContactModel(Base):
    __tablename__ = 'Contact'
    __table_args__ = {'schema': 'customers'}

    id: Mapped[int] = mapped_column('Id', primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column('Name')

    created_at: Mapped[datetime] = mapped_column('CreatedAt', default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column('UpdatedAt', default=datetime.now(timezone.utc),
                                                 onupdate=datetime.now(timezone.utc))
