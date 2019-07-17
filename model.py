from peewee import SqliteDatabase, Model, IntegerField, DoubleField, DateTimeField, datetime as peewee_datetime
from config import DB_NAME, FOR_TEST_DB

db = SqliteDatabase(DB_NAME)

class ExRate(Model):
    class Meta:
        database = db
        db_table = "ex_rates"
        indexes = (
            (("from_currency", "to_currency"), True),
        )
    
    from_currency = IntegerField()
    to_currency = IntegerField()
    rate = DoubleField()
    updated = DateTimeField(default = peewee_datetime.datetime.now)

    def __str__(self):
        return f"{self.from_currency} => {self.to_currency}: {self.rate}"

def init_db():
    db.drop_tables(ExRate)
    ExRate.create_table()
    ExRate.create(from_currency = FOR_TEST_DB["from_currency"], to_currency = FOR_TEST_DB["to_currency"], rate = FOR_TEST_DB["rate"])
    print("DB created!")