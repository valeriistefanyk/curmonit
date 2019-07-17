from peewee import SqliteDatabase, Model, IntegerField, DoubleField, DateTimeField, datetime as peewee_datetime
from config import DB_NAME, TEST_CUR

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
    ExRate.create(from_currency = TEST_CUR["USD"]["from_currency"], to_currency = TEST_CUR["USD"]["to_currency"], rate = TEST_CUR["USD"]["rate"])
    ExRate.create(from_currency = TEST_CUR["EUR"]["from_currency"], to_currency = TEST_CUR["EUR"]["to_currency"], rate = TEST_CUR["EUR"]["rate"])
    ExRate.create(from_currency = TEST_CUR["RUB"]["from_currency"], to_currency = TEST_CUR["RUB"]["to_currency"], rate = TEST_CUR["RUB"]["rate"])
    ExRate.create(from_currency = TEST_CUR["TST"]["from_currency"], to_currency = TEST_CUR["TST"]["to_currency"], rate = TEST_CUR["TST"]["rate"])
    print("DB created!")