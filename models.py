from peewee import SqliteDatabase, Model, IntegerField, CharField, TextField, DoubleField, DateTimeField, datetime as peewee_datetime
from config import DB_NAME, TEST_CUR

db = SqliteDatabase(DB_NAME)

class _Model(Model):
    class Meta:
        database = db

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

class ApiLog(_Model):
    class Meta:
        db_table = "api_logs"
    request_url = CharField()
    request_data = TextField(null = True)
    request_method = CharField(max_length = 50)
    request_headers = TextField(null = True)
    response_text = TextField(null = True)
    created = DateTimeField(index = True, default = peewee_datetime.datetime.now())
    finished = DateTimeField()
    error = TextField(null = True)

class ErrorLog(_Model):
    class Meta:
        db_table = "error_logs"
    request_url = TextField()
    request_data = TextField(null = True)
    request_method = CharField(max_length = 50)
    error = TextField()
    traceback = TextField(null = True)
    created = DateTimeField(index = True, default = peewee_datetime.datetime.now)

def init_db():
    # db.drop_tables(ExRate)
    ExRate.drop_table()
    ExRate.create_table()
    ExRate.create(from_currency = TEST_CUR["USD"]["from_currency"], to_currency = TEST_CUR["USD"]["to_currency"], rate = TEST_CUR["USD"]["rate"])
    ExRate.create(from_currency = TEST_CUR["EUR"]["from_currency"], to_currency = TEST_CUR["EUR"]["to_currency"], rate = TEST_CUR["EUR"]["rate"])
    ExRate.create(from_currency = TEST_CUR["RUB"]["from_currency"], to_currency = TEST_CUR["RUB"]["to_currency"], rate = TEST_CUR["RUB"]["rate"])
   
    for m in (ApiLog, ErrorLog):
        m.drop_table()
        m.create_table()

    print("DB created!")