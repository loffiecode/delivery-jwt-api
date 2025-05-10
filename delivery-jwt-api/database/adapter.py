from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import update, select
from sqlalchemy.orm import joinedload

from typing import Optional, Dict, Any, Union
from models import Order, Delivery, \
        DB, User
from misc import generateSalt, hashPassword
from config import PROHIBITED_DATA_UPDATE_DELIVERY


class DatabaseAdapter:
    def __init__(self, database_url: str):
        self._engine = create_async_engine(database_url, echo=False)
        self._session = async_sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )
        self._db = DB
    
    async def init(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(self._db.metadata.create_all)

    async def createOrder(
            self, 
            name: str,
            pickup: str,
            delivery: str, 
            weight: int, 
            dimensions: str,
            description: Optional[str] = None
        ) -> Order:
        """Создание нового ордера

        :param name: Имя заказа
        :type name: str
        :param pickup: Начальный адрес
        :type pickup: str
        :param delivery: Адрес доставки
        :type delivery: str
        :param weight: Вес доставки
        :type weight: int
        :param dimensions: Размеры посылки
        :type dimensions: str
        :param description: Описание посылки, defaults to None
        :type description: Optional[str], optional
        :return: объект Order
        :rtype: Order
        """
        async with self._session() as session:
            order = Order(
                Description = description,
                Name = name,
                PickUpAddress = pickup,
                DeliveryAddress = delivery,
                Weight = weight,
                Dimensions = dimensions
            )
            session.add(order)
            await session.flush()
            session.add(Delivery(ID=order.ID))  
            await session.commit()
            return order
                    
    async def getOrder(self, order_id: int) -> Optional[Order]:
        """Возвращает объект Order при его наличии

        :param order_id: id ордера
        :type order_id: int
        :return: Возвращает объект Order при его наличии
        :rtype: Optional[Order]
        """
        async with self._session() as session:
            result = await session.execute(
                select(Order).where(Order.ID == order_id)
                    .options(joinedload(Order.delivery))
        )
            return result.scalar()

    async def updateDelivery(
            self, 
            order_id: int, 
            **data: Dict[str, Any]
        ) -> bool:
        """Обновляет информацию о доставке

        :param order_id: ID доставки
        :type order_id: int
        :return: True если успешно, в противном случае False
        :rtype: bool
        """
        async with self._session() as session:
            result = await session.execute(
                    select(Delivery).where(Delivery.ID == order_id)
                )
            delivery = result.scalar()
            if not delivery or not data:
                    return False
            elif any(value in PROHIBITED_DATA_UPDATE_DELIVERY for value in data.values()):
                return False
            await session.execute(
                update(Delivery).where(Delivery.ID == order_id).values(**data)
            )                    
            await session.commit()
            return True
    
    async def deleteOrder(self, order_id: int) -> bool:
        """Удаляет Order

        :param order_id: ID ордера
        :type order_id: int
        :return: True если успешно, в противном случае False
        :rtype: bool
        """
        async with self._session() as session:
            result = await session.execute(
            select(Order).where(Order.ID == order_id)
            )
            order = result.scalar()
            if not order:
                return False
            await session.delete(order)
            await session.commit()
            return True


    async def getUser(self, username: str) -> User:
        """Возвращает объект User

        :param username: Имя пользователя
        :type username: str
        :return: Объект User
        :rtype: User
        """
        async with self._session() as session:
            result = await session.execute(select(User).where(User.Username == username))
            return result.scalar()

    async def createUser(self, username: str, password: str) -> None:
        """Создает нового пользователя

        :param username: Имя пользователя
        :type username: str
        :param password: Пароль пользователя
        :type password: str
        :return: None
        :rtype: None
        """
        async with self._session() as session:
            salt = generateSalt()
            hashed = hashPassword(password, salt)
            user = User(
                Username=username,
                Salt=salt,
                Password=hashed
            )
            session.add(user)
            await session.commit()