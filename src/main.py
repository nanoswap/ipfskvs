from faker import Faker
import datetime
import uuid
from models.index import Index
from models.store import Store
from sample_pb2 import Example, Type

Faker.seed(0)
fake = Faker()

if __name__ == "__main__":
   index = Index(
      prefix="loan",
      index={
         "borrower": uuid.uuid4(),
         "lender": uuid.uuid4()
      }, subindex=Index(
         index={
               "loan": uuid.uuid4()
         }, subindex=Index(
               index={
                  "payment": uuid.uuid4()
         })
      )
   )

   print(index.get_filename())
   print(Index.from_filename(index.get_filename(), has_prefix=True).get_filename())

   data = Example(type=Type.BUZZ, content="fizz")
   store = Store(index=index, writer=data)
   store.add()
   store2 = Store(index=index, reader=Example())
   store2.read()
   print(store2.reader)
