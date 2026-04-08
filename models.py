from sqlalchemy import Date, Float, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data_compra: Mapped[Date] = mapped_column(Date, nullable=False)
    mes_ano: Mapped[str] = mapped_column(String(7), nullable=False, index=True)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    categoria: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    source_file: Mapped[str] = mapped_column(String(150), nullable=False)
    tx_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)

    __table_args__ = (
        UniqueConstraint("tx_hash", name="uq_transactions_tx_hash"),
    )
