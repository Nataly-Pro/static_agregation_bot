from motor.motor_asyncio import AsyncIOMotorClient


"""Подключение к БД MongoDB: 
при развертывании на удаленном сервере поменять 'localhost:27017' на IP адрес сервера,
имя коллекции 'salary', база данных 'salary_db'. 
"""

uri = "mongodb://localhost:27017/"
cluster = AsyncIOMotorClient(uri)
collection = cluster.salary_db.salary

