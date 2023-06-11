from datetime import timedelta, datetime
from sqlalchemy import create_engine, MetaData, Table, Integer, Column, String, insert, select, update, and_, Float


class DataBase:
    engine = create_engine(url="postgresql+psycopg2://postgres:root@localhost/partner_bot", echo=False)

    metadata = MetaData()

    client_table = Table(
        "client_information",
        metadata,
        Column("id", Integer, autoincrement=True, primary_key=True),
        Column("phone_number", String),
        Column("link10", String),
        Column("link25", String),
        Column("client_name", String),
        Column("user_id", Integer),
        Column("spam1", Float),
        Column("spam2", Float),
        Column("spam3", Float)
    )

    def create_table(self) -> None:
        return self.metadata.create_all(self.engine)

    def add_phone_number(self, phone_number: str) -> None:
        statement = insert(self.client_table).values(phone_number=phone_number)
        with self.engine.connect() as connection:
            connection.execute(statement)
            return connection.commit()

    def check_phone_number(self, phone_number: str) -> str | None:
        statement = select(self.client_table).where(self.client_table.c.phone_number == phone_number)
        with self.engine.connect() as connection:
            result = connection.execute(statement).fetchone()
            return result[1] if result is not None else False

    def update_link10(self, phone_number: str, link10: str) -> None:
        statement = update(self.client_table).values(link10=link10).where(self.client_table.c.phone_number == phone_number)
        with self.engine.connect() as connection:
            connection.execute(statement)
            return connection.commit()

    def check_link10(self, phone_number: str, link10: str) -> str | None:
        statement = select(self.client_table).where(and_(
            self.client_table.c.phone_number == phone_number,
            self.client_table.c.link10 == link10
        ))
        with self.engine.connect() as connection:
            result = connection.execute(statement).fetchone()
            return result[2] if result is not None else False

    def update_link25(self, phone_number: str, link25: str) -> None:
        statement = update(self.client_table).values(link25=link25).where(self.client_table.c.phone_number == phone_number)
        with self.engine.connect() as connection:
            connection.execute(statement)
            return connection.commit()

    def check_link25(self, phone_number: str, link25: str) -> str | None:
        statement = select(self.client_table).where(and_(
            self.client_table.c.phone_number == phone_number,
            self.client_table.c.link25 == link25
        ))
        with self.engine.connect() as connection:
            result = connection.execute(statement).fetchone()
            return result[3] if result is not None else False

    def update_client_name(self, phone_number: str, client_name: str) -> None:
        statement = update(self.client_table).values(client_name=client_name).where(self.client_table.c.phone_number == phone_number)
        with self.engine.connect() as connection:
            connection.execute(statement)
            return connection.commit()

    def check_client_name(self, phone_number: str, client_name: str) -> str | None:
        statement = select(self.client_table).where(and_(
            self.client_table.c.phone_number == phone_number,
            self.client_table.c.client_name == client_name
        ))
        with self.engine.connect() as connection:
            result = connection.execute(statement).fetchone()
            return result[4] if result is not None else False

    def update_user_id(self, phone_number: str, user_id: int) -> None:
        statement = update(self.client_table).values(user_id=user_id).where(self.client_table.c.phone_number == phone_number)
        with self.engine.connect() as connection:
            connection.execute(statement)
            return connection.commit()

    def check_user_id(self, phone_number: str, user_id: int) -> str | None:
        statement = select(self.client_table).where(and_(
            self.client_table.c.phone_number == phone_number,
            self.client_table.c.user_id == user_id
        ))
        with self.engine.connect() as connection:
            result = connection.execute(statement).fetchone()
            return result[5] if result is not None else False

    def get_all_clients(self) -> list:
        statement = select(self.client_table)
        with self.engine.connect() as connection:
            return connection.execute(statement).fetchall()

    def update_spam_1(self, phone_number: str, spam1: datetime) -> None:
        upd_spam1 = update(self.client_table).values(
            spam1=(spam1 + timedelta(days=3)).timestamp(),  #d
        ).where(self.client_table.c.phone_number == phone_number)
        with self.engine.connect() as connection:
            connection.execute(upd_spam1)
            return connection.commit()

    def get_spam_1(self, phone_number: str) -> float:
        get_spam1 = select(self.client_table.c.spam1).where(self.client_table.c.phone_number == phone_number)
        with self.engine.connect() as connection:
            return connection.execute(get_spam1).fetchone()[0]

    def update_spam_2(self, phone_number: str, spam1: float) -> None:
        upd_spam2 = update(self.client_table).values(
            spam2=(datetime.fromtimestamp(spam1) + timedelta(days=7)).timestamp(), #
        ).where(self.client_table.c.phone_number == phone_number)
        with self.engine.connect() as connection:
            connection.execute(upd_spam2)
            return connection.commit()

    def get_spam_2(self, phone_number: str) -> float:
        get_spam2 = select(self.client_table.c.spam2).where(self.client_table.c.phone_number == phone_number)
        with self.engine.connect() as connection:
            return connection.execute(get_spam2).fetchone()[0]

    def update_spam_3(self, phone_number: str, spam2: float) -> None:
        upd_spam3 = update(self.client_table).values(
            spam3=(datetime.fromtimestamp(spam2) + timedelta(days=3)).timestamp(), #
        ).where(self.client_table.c.phone_number == phone_number)
        with self.engine.connect() as connection:
            connection.execute(upd_spam3)
            return connection.commit()

    def get_spam_3(self, phone_number: str) -> float:
        get_spam3 = select(self.client_table.c.spam3).where(self.client_table.c.phone_number == phone_number)
        with self.engine.connect() as connection:
            return connection.execute(get_spam3).fetchone()[0]

    def drop_table(self) -> None:
        return self.metadata.drop_all(self.engine)





