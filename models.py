from peewee import SqliteDatabase, Model, IntegerField, CharField, TextField, DoubleField, DateTimeField, datetime as peewee_datetime
from config import DB_NAME, CODE_DICT

db = SqliteDatabase(DB_NAME)

class _Model(Model):
    class Meta:
        database = db

class ExRate(_Model):
    class Meta:
        db_table = "ex_rates"
        indexes = (
            (("from_currency", "to_currency"), True),
        )
    
    from_currency = IntegerField()
    to_currency = IntegerField()
    rate = DoubleField()
    updated = DateTimeField(default = peewee_datetime.datetime.now)
    module = CharField(max_length = 100)

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

    def json(self):
        data = self.__data__
        return data

class ErrorLog(_Model):
    class Meta:
        db_table = "error_logs"
    request_url = TextField()
    request_data = TextField(null = True)
    request_method = CharField(max_length = 50)
    error = TextField()
    traceback = TextField(null = True)
    created = DateTimeField(index = True, default = peewee_datetime.datetime.now)
    
    def json(self):
        data = self.__data__
        return data

def init_db():
    # db.drop_tables(ExRate)
    ExRate.drop_table()
    ExRate.create_table()
    ExRate.create(from_currency = CODE_DICT["USD"], to_currency = CODE_DICT["UAH"], rate = 1.0, module = "privatbank_json_api")
    ExRate.create(from_currency = CODE_DICT["EUR"], to_currency = CODE_DICT["UAH"], rate = 1.0, module = "privatbank_xml_api")
    ExRate.create(from_currency = CODE_DICT["RUB"], to_currency = CODE_DICT["UAH"], rate = 1.0, module = "monobank_api")
    ExRate.create(from_currency = CODE_DICT["EUR"], to_currency = CODE_DICT["USD"], rate = 1.0, module = "monobank_api")
    ExRate.create(from_currency = CODE_DICT["BTC"], to_currency = CODE_DICT["USD"], rate = 1.0, module = "privatbank_json_api")
    ExRate.create(from_currency = CODE_DICT["BTC"], to_currency = CODE_DICT["UAH"], rate = 1.0, module = "cryptonator_api")


    for m in (ApiLog, ErrorLog):
        m.drop_table()
        m.create_table()

    print("DB created!")